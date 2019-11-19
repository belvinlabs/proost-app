import datetime
import pickle

from google.cloud import datastore
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from models.app_main import User

datastore_client = datastore.Client()


def get_user_api_credentials(user_id):
    user = User.query.get(int(user_id))

    if not user.google_credentials:
        return None

    return pickle.loads(user.google_credentials)


def get_calendar_api_client(user_id):
    credentials = get_user_api_credentials(user_id)

    if not credentials:
        return None

    if credentials.expired:
        credentials.refresh(Request())

    return build('calendar', 'v3', credentials=credentials, cache_discovery=False)


def get_user_api_client(user_id):
    credentials = get_user_api_credentials(user_id)

    if not credentials:
        return None

    if credentials.expired:
        credentials.refresh(Request())

    return build('admin', 'directory_v1', cache_discovery=False, credentials=credentials)
