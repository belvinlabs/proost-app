from flask import Blueprint, session, render_template, abort, redirect, request, url_for, jsonify
from flask_login import login_user, login_required, current_user
import google_auth_oauthlib.flow
import jwt
import pickle

from data import api_credentials
from models.app_main import User as UserModel
from models.base import db
from utils import env
from utils.common import get_file_full_path


CLIENT_SECRETS_FILE = get_file_full_path('google_client_secret.json')
REQUIRED_SCOPES = ['openid',
                   'https://www.googleapis.com/auth/userinfo.email',
                   'https://www.googleapis.com/auth/userinfo.profile',
                   'https://www.googleapis.com/auth/calendar.readonly',
                   'https://www.googleapis.com/auth/admin.directory.user.readonly']

auth = Blueprint('auth', __name__)


class User:
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def get_id(self):
        return self.id


def get_user_by_id(user_id):
    user = UserModel.query.get(int(user_id))

    return user


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'scopes': credentials.scopes}


@auth.route('/auth/google/init')
def auth_init():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                                   REQUIRED_SCOPES)

    flow.redirect_uri = url_for('auth.auth_callback', _external=True)

    authorization_url_kwargs = {'access_type': 'offline',
                                'include_granted_scopes': 'true'}

    
    authorization_url_kwargs['prompt'] = 'consent'

    authorization_url, state = flow.authorization_url(
        **authorization_url_kwargs)

    session['state'] = state

    return redirect(authorization_url)


@auth.route('/auth/google/callback')
def auth_callback():
    if request.args.get('error') == 'access_denied':
        return redirect('/')

    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE,
                                                                   scopes=REQUIRED_SCOPES,
                                                                   state=state)

    flow.redirect_uri = url_for('auth.auth_callback', _external=True)

    flow.fetch_token(authorization_response=request.url)

    # this token came from Google, so don't worry aboue re-verifying its signature in this context
    id_data = jwt.decode(flow.credentials.id_token, verify=False)

    user_email = None if not id_data['email_verified'] else id_data['email']

    if not user_email:
        return redirect('/')

    user = UserModel.query.filter_by(email=user_email).first()

    if user:
        user.name = id_data['name']
        user.sub = id_data['sub']
        user.given_name = id_data['given_name']
        user.family_name = id_data['family_name']
        user.picture_url = id_data['picture']
    else:
        user = UserModel(
          email=user_email,
          sub=id_data['name'],
          name=id_data['name'],
          given_name=id_data['given_name'],
          family_name=id_data['family_name'],
          picture_url=id_data['picture']
        )
    db.session.add(user)
    db.session.commit()
    login_user(user)

    # refresh token only provided on initial auth
    if flow.credentials.refresh_token:
        user.google_credentials = pickle.dumps(flow.credentials)
        db.session.commit()

    return redirect('%s/database' % ('http://localhost:3000' if env.is_local() else ''))


@auth.route('/auth/google/check')
@login_required
def auth_check():
    # See https://developers.google.com/calendar/quickstart/python
    calendar_client = api_credentials.get_calendar_api_client(current_user.id)

    events_result = calendar_client.events().list(calendarId='primary',
                                                  maxResults=10,
                                                  singleEvents=True,
                                                  orderBy='startTime'
                                                  ).execute()

    events = events_result.get('items', [])

    return jsonify(events)
