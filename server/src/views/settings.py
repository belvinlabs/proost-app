import datetime

from flask import Blueprint, session, request, jsonify
from flask_login import login_required, current_user

from models.app_main import Settings
from models.base import db

from controllers.syncs import start_calendar_sync_task


settings = Blueprint('settings', __name__)


def _to_json(settings):
    return jsonify({
        'synced_calendars': settings.synced_calendars
    })


def get_settings(user_id):
    settings = Settings.query.filter_by(user_id=current_user.id).first()

    if settings:
        return settings

    settings = Settings(user_id=user_id,
                        synced_calendars=[])

    db.session.add(settings)
    db.session.commit()

    return settings


@settings.route('/api/settings/mine')
@login_required
def get_settings_handler():
    return _to_json(get_settings(current_user.id))


@settings.route('/api/settings/mine', methods=['POST'])
@login_required
def update_settings():
    # TODO: Kick off sync here.
    settings = get_settings(current_user.id)
    settings.synced_calendars = request.get_json()['synced_calendars']

    start_calendar_sync_task(request, settings)
    json_response = _to_json(settings)
    return json_response
