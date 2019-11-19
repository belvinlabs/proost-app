import requests
import logging
import string
import random
from models.base import db
from utils.app import app
from utils.common import random_password
from models.app_main import UserMetabase

# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

base_url = None

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def authenticateMetabaseUser(username, password):
    global base_url
    url = f'http://{base_url}/api/session'
    return requests.post(url, json={
        'username': username,
        'password': password
    })


def createMetabaseGroup(username, session):
    global base_url
    groupname = username + '_group'
    group = {
        'name': groupname
    }
    url = f'http://{base_url}/api/permissions/group'
    return requests.post(
        url,
        json=group,
        headers={
            'X-Metabase-Session': session
        }
    )


def createMetabaseUser(first, last, email, pwd, group_id, session):
    global base_url
    url = f'http://{base_url}/api/user'
    user = {
        'first_name': first,
        'last_name': last,
        'email': email,
        'password': pwd,
        # Group 1 is the all user group and is required.
        'group_ids': [1, group_id]
    }
    result = requests.post(
        url,
        json=user,
        headers={
            'X-Metabase-Session': session
        }
    )
    return result


def createDatabase(email, db_host, db_port, db_name, db_user, db_password, session):
    global base_url
    endpoint = '/api/database/'
    url = f'http://{base_url}{endpoint}'



    database = {
        "name": email + " db",
        "engine": "mysql",
        "details": {
            "host": db_host,
            "port": db_port,
            "dbname": db_name,
            "user": db_user,
            "password": db_password
        }
    }
    return requests.post(
        url,
        json=database,
        headers={
            'X-Metabase-Session': session
        }
    )


def getGraph(session):
    global base_url
    endpoint = '/api/permissions/graph'
    url = f'http://{base_url}{endpoint}'
    return requests.get(
        url,
        headers={
            'X-Metabase-Session': session
        }
    )


def putGraph(graph, session):
    global base_url
    endpoint = '/api/permissions/graph'
    url = f'http://{base_url}{endpoint}'
    return requests.put(
        url,
        json=graph,
        headers={
            'X-Metabase-Session': session
        }
    )


def create_metabase_session(user):
    global base_url
    base_url = app.config['METABASE_URL']
    
    metabase_user = UserMetabase.query.get(user.id)
    authentication_response = authenticateMetabaseUser(metabase_user.email, metabase_user.password)

    # This value can be used to set a cookie on the users browser that will automatically log the user in to metabase
    new_user_session = authentication_response.json()['id']
    return new_user_session


def createMetabase(proost_user, local=False):
    global base_url
    # root user
    username = app.config['METABASE_USERNAME']
    password = app.config['METABASE_PASSWORD']
    base_url = app.config['METABASE_URL']

    # New metabase user details. Email needs to be unique
    newuser_first = proost_user.given_name
    newuser_last = proost_user.family_name
    newuser_email = randomString() + '_' + proost_user.email

    # There is a password generator in the Utils
    pwd = random_password()

    metabase_user = UserMetabase(
        user_id=proost_user.id,
        email=newuser_email,
        password=pwd
    )

    db.session.add(metabase_user)
    db.session.commit()

    # TODO this is assuming one database, which might change over time
    proost_db = proost_user.databases[0]
    # Use the user details
    db_host = 'host.docker.internal' if local else proost_db.host
    db_port = proost_db.port
    db_name = proost_db.database
    db_user = proost_db.username
    db_password = proost_db.password

    # def create_user():
    authentication_response = authenticateMetabaseUser(username, password)
    session = authentication_response.json()['id']

    group_response = createMetabaseGroup(newuser_email, session)
    group_id = group_response.json()['id']
    resp = createMetabaseUser(newuser_first, newuser_last,
                              newuser_email, pwd, group_id, session)

    resp = createDatabase(newuser_email, db_host, db_port,
                          db_name, db_user, db_password, session)
    database = resp.json()
    database_id = database['id']

    resp = getGraph(session)
    graph = resp.json()
    graph['groups'][group_id] = {
        database_id: {
            'schemas': 'all',
            'native': 'write'
        }
    }
    resp = putGraph(graph, session)

    graph = resp.json()
    # Remove database from the all users group
    graph['groups']['1'][str(database_id)] = {
        'native': 'none',
        'schemas': 'none'
    }
    resp = putGraph(graph, session)

    authentication_response = authenticateMetabaseUser(newuser_email, pwd)

    # This value can be used to set a cookie on the users browser that will automatically log the user in to metabase
    new_user_session = authentication_response.json()['id']
    
    return new_user_session
