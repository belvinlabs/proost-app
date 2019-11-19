import random

from flask import Blueprint, session, request, jsonify
from flask_login import login_required, current_user

queries = Blueprint('queries', __name__)


STUBBED_HOURS_RESPONSE = [
  {
    'date': '2019-10-14',
    'confirmed_meeting_hours': 3,
    'unconfirmed_meeting_hours': 1.5,
    'remaining_hours': 3.5
  },
  {
    'date': '2019-10-15',
    'confirmed_meeting_hours': 2,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 5
  },
  {
    'date': '2019-10-16',
    'confirmed_meeting_hours': 0.5,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 6.5
  },
  {
    'date': '2019-10-17',
    'confirmed_meeting_hours': 4,
    'unconfirmed_meeting_hours': 0,
    'remaining_hours': 4
  },
  {
    'date': '2019-10-18',
    'confirmed_meeting_hours': 3,
    'unconfirmed_meeting_hours': 1.5,
    'remaining_hours': 3.5
  },
  {
    'date': '2019-10-19',
    'confirmed_meeting_hours': 2,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 5
  },
  {
    'date': '2019-10-20',
    'confirmed_meeting_hours': 0.5,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 6.5
  },
  {
    'date': '2019-10-21',
    'confirmed_meeting_hours': 4,
    'unconfirmed_meeting_hours': 0,
    'remaining_hours': 4
  },
  {
    'date': '2019-10-22',
    'confirmed_meeting_hours': 3,
    'unconfirmed_meeting_hours': 1.5,
    'remaining_hours': 3.5
  },
  {
    'date': '2019-10-23',
    'confirmed_meeting_hours': 2,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 5
  },
  {
    'date': '2019-10-24',
    'confirmed_meeting_hours': 0.5,
    'unconfirmed_meeting_hours': 1,
    'remaining_hours': 6.5
  },
  {
    'date': '2019-10-25',
    'confirmed_meeting_hours': 4,
    'unconfirmed_meeting_hours': 0,
    'remaining_hours': 4
  }
]


@queries.route('/api/query')
@login_required
def get_calendars():
  # query = request.args.get('query')

  random.shuffle(STUBBED_HOURS_RESPONSE)

  return jsonify(STUBBED_HOURS_RESPONSE)
