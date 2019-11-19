# Native
import re
import json

# Installed
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.engine.url import URL as SqlAlchemyURL
from flask_sqlalchemy import BaseQuery


# From app
from models.base import db


def get_db_url(user_database):
    return str(SqlAlchemyURL(
        drivername=user_database['drivername'],
        username=user_database['username'],
        password=user_database['password'],
        database=user_database['database'],
        host=user_database['host'],
        port=user_database['port'],
        # query={
        #   'unix_socket': '/cloudsql/{}'.format(user_database['query'])
        # }
    )) + '?charset=utf8mb4'


def get_all_user_db_urls(app):
    user_database_urls = {}
    query = f'SELECT `drivername`, `username`, `password`, `database`, `host`, `port`, `query`, `user_id` FROM ' \
            f'`{app.config["APP_DB_NAME"]}`.user_databases'
    databases = db.engine.execute(query).fetchall()
    for database in databases:
        user = {
            'drivername': database[0],
            'username': database[1],
            'password': database[2],
            'database': database[3],
            'host': database[4],
            'port': database[5],
            'query': database[6],
            'user_id': database[7],
        }
        url = get_db_url(user)
        user_database_urls[user['user_id']] = url
    return user_database_urls


EMAIL_REGEX = re.compile(r"[\.\/\\@]", re.IGNORECASE)


def email_to_name(email):
    return re.sub(EMAIL_REGEX, '_', email)
