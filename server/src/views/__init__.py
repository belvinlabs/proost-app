from views.auth import auth
from views.calendars import calendars
from views.databases import databases
from views.queries import queries
from views.settings import settings
from views.syncs import syncs
from views.user import user

blueprints = [auth, user, calendars, queries, settings, syncs, databases]
