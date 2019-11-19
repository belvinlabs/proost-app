from datetime import datetime, timedelta

from flask import Blueprint, session, request, jsonify, make_response
from flask_login import login_required, current_user

from controllers.databases import get_user_database
from controllers.metabase import create_metabase_session
from utils.app import app

databases = Blueprint('databases', __name__)

@databases.route('/api/databases/mine')
@login_required
def get_my_database():


  user_database = get_user_database(current_user, 'localhost' in request.host)
  metabase_session = create_metabase_session(current_user)

  host = request.host

  resp = make_response(jsonify({
    'host': user_database.host,
    'port': user_database.port,
    'username': user_database.username,
    'password': user_database.password,
    'name': user_database.database
  }))

  exp = datetime.now() + timedelta(days=31)
  if 'localhost' in request.host:
    resp.set_cookie('metabase.SESSION', value=metabase_session, expires=exp)
  else:
    resp.set_cookie('metabase.SESSION', value=metabase_session, expires=exp, domain='.'+app.config['DOMAIN_BASE'])
  return resp
