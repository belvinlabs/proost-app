import time

from flask_login import login_required, current_user
from flask import Blueprint, session, request


from utils.app import jsonify, app
from utils.tasks import create_task
from data.api_credentials import get_calendar_api_client, get_user_api_client
from models.base import db
from models.app_main import User, Settings
from models.user_calendar import CalendarEvents, CalendarEventAttendees, CalendarUser, CalendarUserAlias
from models.app_sync import Sync
from controllers.syncs import calendar_sync_main, start_calendar_sync_task, CALENDAR_SYNC_HANDLER_URL

from sqlalchemy.orm import sessionmaker


syncs = Blueprint('syncs', __name__)

# TODO Store and use synctokens
@syncs.route('/api/syncs/mine')
@login_required
def list_syncs():
    user_id = current_user.id
    sync = Sync.query.filter_by(user_id=current_user.id).all()
    return jsonify(sync, fields_to_expand=['tasks'])

@syncs.route('/api/syncs/last')
@login_required
def last_syncs():
    user_id = current_user.id
    sync = Sync.query.filter_by(user_id=current_user.id).order_by(Sync.time_created.desc()).first()
    return jsonify(sync, fields_to_expand=['tasks'])


@syncs.route('/api/syncs', methods=['POST'])
def create_sync():
    user_id = current_user.id
    session = app.db.session
    settings = session.query(Settings).get(user_id)
    start_calendar_sync_task(request, settings)
    data = request.json
    return jsonify(data)


@syncs.route(CALENDAR_SYNC_HANDLER_URL, methods=['POST'])
def task_calendar_sync():
    # Getting the details about the sync job
    data = request.json
    user_id = data['user_id']
    calendars = data['calendars']

    result = calendar_sync_main(user_id, calendars)

    return jsonify(result)
