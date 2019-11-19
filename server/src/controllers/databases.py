from sqlalchemy_utils import database_exists, drop_database, create_database

from models.app_main import UserDatabase
from models.base import db
from utils.app import app
from utils.common import random_password
from utils.database import get_db_url, email_to_name
from utils.enums import APIErrorTypes
from utils.errors import APIError

from controllers.metabase import createMetabase


def initialize_database(user, local):
    new_db_name = email_to_name(user.email)
    new_password = random_password()

    # Create a user that will have access to the new datase
    new_database = UserDatabase(
        drivername='mysql+pymysql',
        username=new_db_name,
        password=new_password,
        host=app.config["APP_DB_HOST"],
        port=app.config["APP_DB_PORT"],
        database=new_db_name,
        query=app.config["CLOUD_SQL_CONNECTION_NAME"],
        user_id=user.id
    )

    url = get_db_url({
        'drivername': 'mysql+pymysql',
        'username': app.config["APP_DB_USER"],
        'password': app.config["APP_DB_PASS"],
        'host': app.config["APP_DB_HOST"],
        'port': app.config["APP_DB_PORT"],
        'database': new_db_name,
        'query': app.config["CLOUD_SQL_CONNECTION_NAME"]
    })

    # Step 1: create the new database
    if database_exists(url):
        raise APIError(
            http_code=409,
            error_type_key=APIErrorTypes.database_already_exists,
            message=f'Trying to create database {new_db_name} for user {user.email}, but the database already exists'
        )
    else:
        create_database(url)

    # Step 2: create all the tables in the new database
    # Setting the config to the new database url is a hack
    # to make sure SQLALCHAMY does all the heavy lifting
    app.config['SQLALCHEMY_BINDS']['user_db'] = url
    db.create_all(['user_db'])

    # Step 3: Create the new user so that someone can connect
    create_user_query = f'CREATE USER \'{new_db_name}\'@\'%%\' ' \
                        f'IDENTIFIED WITH mysql_native_password ' \
                        f'BY \'{new_password}\';'
    db.engine.execute(create_user_query)

    # Step 4: Give the user the right privileges
    priveleges = [
        'CREATE',
        'INSERT',
        'SELECT',
        'UPDATE',
        'ALTER',
        'DROP',
        'REFERENCES'
    ]
    priveleges_string = ', '.join(priveleges)

    priveleges_string = 'ALL PRIVILEGES'

    grant_perms_query = f'GRANT {priveleges_string} ON {new_db_name}.* ' \
                        f'TO \'{new_db_name}\'@\'%%\';'

    db.engine.execute(grant_perms_query)

    # Step 5: Create the alembic table for migration purposes
    alembic_create_query = f'CREATE TABLE `{new_db_name}`.`alembic_version` ' \
                           f'(' \
                           f'  `version_num` varchar(32) NOT NULL,' \
                           f'  PRIMARY KEY (`version_num`)' \
                           f')'
    db.engine.execute(alembic_create_query)

    # Step 6: Get the data that should be in the new alembic table
    alembic_select_query = f'SELECT `version_num` FROM ' \
                           f'`{app.config["EXAMPLE_DB_NAME"]}`.alembic_version'
    versions = db.engine.execute(alembic_select_query).fetchall()

    # Step 7: Insert the data into the new alembic table
    if len(versions) > 0:
        alembic_insert_query = f'INSERT INTO `{new_db_name}`.' \
                               f'`alembic_version` ' \
                               f'(`version_num`)\n' \
                               f'VALUES\n'
        for row in versions:
            alembic_insert_query += f'(\'{row[0]}\')'
        db.engine.execute(alembic_insert_query)

    # Step 8: Add the user to the session. As the relationship
    # to a UserDatabase object is created in the new_database creation,
    # adding the User object user to the session and committing it will
    # create a new User and UserDatabase row
    db.session.add(new_database)
    db.session.commit()

    createMetabase(user, local)

    return new_database


def get_user_database(user, local):
    # using more elaborate syntax here because `UserDatabase.query` is a table column.
    existing_database = db.session.query(
        UserDatabase).filter_by(user_id=user.id).one_or_none()

    if existing_database:
        return existing_database



    return initialize_database(user, local)
