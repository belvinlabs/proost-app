# Native
import os
import logging
from logging.config import dictConfig

# Installed
from sqlalchemy.engine.url import URL as SqlAlchamyURL
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from dotenv import load_dotenv

# From app
from utils.database import get_all_user_db_urls, get_db_url


def load_customer_db_config(app):
    dbs = get_all_user_db_urls(app)
    if 'SQLALCHEMY_MULTI_DB' in app.config:
        multi_db = app.config['SQLALCHEMY_MULTI_DB']
        app.config['SQLALCHEMY_MULTI_DB'] = multi_db
    else:
        app.config['SQLALCHEMY_MULTI_DB'] = {}
    app.config['SQLALCHEMY_MULTI_DB']['user_db'] = dbs


def set_config_db(app):
    db_user = app.config["APP_DB_USER"]
    db_pass = app.config["APP_DB_PASS"]
    app_db_name = app.config["APP_DB_NAME"]
    db_host = app.config["APP_DB_HOST"]
    db_port = app.config["APP_DB_PORT"]
    cloud_sql_connection_name = app.config["CLOUD_SQL_CONNECTION_NAME"]
    example_db_name = app.config["EXAMPLE_DB_NAME"]

    app_url = get_db_url({
        'drivername': 'mysql+pymysql',
        'username': db_user,
        'password': db_pass,
        'database': app_db_name,
        'host': db_host,
        'port': db_port,
    })

    app.config['SQLALCHEMY_DATABASE_URI'] = app_url
    example_db_url = get_db_url({
        'drivername': 'mysql+pymysql',
        'username': db_user,
        'password': db_pass,
        'database': example_db_name,
        'host': db_host,
        'port': db_port,
    })

    app.config['SQLALCHEMY_EXAMPLE_CUSTOMER_DB_URI'] = example_db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_BINDS'] = {
        'user_db': app.config['SQLALCHEMY_EXAMPLE_CUSTOMER_DB_URI']
    }


def set_config(app):
    load_dotenv()
    dirname = os.path.dirname(__file__)

    app_filename = '../app.yaml'
    stream = open(os.path.join(dirname, app_filename), 'r')

    env_vars = {}
    logging.info('The following environment variables need to be defined for '
                 'the app to run (as per app.yaml) and can be accessed '
                 'through '
                 'app.config[VARIABLE]:')
    yaml_env_vars = yaml.load(stream, Loader)['env_variables']
    for (variable, app_val) in yaml_env_vars.items():
        value = os.getenv(variable)
        env_vars[variable] = value
        if value:
            logging.info(
                f'- {variable} is set from a local environment variable')
            app.config[variable] = value
        elif app_val != 'placeholder':
            logging.info(
                f'- {variable} does not have to be overwritten as it '
                'isn\'t a placeholder')
            app.config[variable] = app_val
        else:
            logging.error(f'- {variable} environment variable is NOT set')
    logging.info('')
    logging.info('You can either set them manually on your local machine, or '
                 'add a .env file to the {GIT_ROOT}/server directory')

    app.config['SECRET_KEY'] = app.config['FLASK_SECRET_KEY']

    set_config_db(app)


def set_logging(app):
    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: '
                          '%(message)s'
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO' if app.config['DEBUG'] else 'WARNING',
            'handlers': ['wsgi']
        }
    })

    logging.info('Log information loaded')
