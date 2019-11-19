from flask import Blueprint, session, request, jsonify
from flask_login import login_required, current_user

from data.api_credentials import get_calendar_api_client, get_user_api_client

calendars = Blueprint('calendars', __name__)


def _is_relevant_calendar(calendar_id, user_email):
  # filters out calendars like `en.usa#holiday@group.v.calendar.google.com` (US Holiday calendars) and
  # `addressbook#contacts@group.v.calendar.google.com` (Contacts).
  #
  # Relevant calendar examples:
  # - {"id": "itsotester3@gmail.com", "summary": "itsotester3@gmail.com"}
  # - {"id": "6e6hrodgbluct03bq6h62sdbf8@group.calendar.google.com", "summary": "My Second Calendar"}
  # - {"id": "itso.io_achdr2ab8qi9hmado0legi54bk@group.calendar.google.com", "summary": "Jon's Second Calendar"}
  # - {"id": "adi07f5ph020mdjvtv07fbinpphe6svf@import.calendar.google.com", "summary": "Brad's example}
  # - {"id": "jon@itso.io", "summary": "jon@itso.io"}

  EXCLUDED_SUFFIXES = [
    '#holiday@group.v.calendar.google.com',
    '#contacts@group.v.calendar.google.com'
  ]

  return not next((suffix for suffix in EXCLUDED_SUFFIXES if calendar_id.endswith(suffix)), None)


@calendars.route('/api/calendars')
@login_required
def get_calendars():
  cal_client = get_calendar_api_client(current_user.id)

  calendars = []
  page_token = None
  ids = []
  while True:
    calendar_list = cal_client.calendarList().list(pageToken=page_token).execute()

    for entry in calendar_list['items']:
      ids.append(entry['id'])
      if _is_relevant_calendar(entry['id'], current_user.email):
        calendars.append({
                           'id': entry['id'],
                           'summary': entry['summary'],
                           'added_to_calendar': True,
                           'user_calendar': entry['id'] == entry['summary']
                        })

    page_token = calendar_list.get('nextPageToken')
    if not page_token:
      break

  user_client = get_user_api_client(current_user.id)

  # TODO is this the best way to get the domain or customer ID for a user?
  domain = current_user.email[current_user.email.find("@") + 1 :]

  get_domain_cals = domain != 'gmail.com'

  while get_domain_cals:
    user_list = user_client.users().list(pageToken=page_token, viewType='domain_public', domain=domain).execute()

    for entry in user_list.get('users', []):
      user_id = entry['primaryEmail']
      if user_id not in ids:
        ids.append(user_id)
        if _is_relevant_calendar(user_id, current_user.email):
          calendars.append({
                            'id': user_id,
                            # As this will be the primary calendar of the user, the summary will be the user_id too
                            'summary': user_id,
                            'added_to_calendar': False,
                            'user_calendar': True
                          })

    page_token = user_list.get('nextPageToken')
    if not page_token:
      break

  return jsonify(calendars)
