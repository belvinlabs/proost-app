# Native
import logging
from logging.config import dictConfig

# Installed
## N/A

# From app
## N/A


def set_logging(app):
#   dictConfig({
#       'version': 1,
#       'formatters': {'default': {
#           'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
#       }},
#       'handlers': {'wsgi': {
#           'class': 'logging.StreamHandler',
#           'stream': 'ext://flask.logging.wsgi_errors_stream',
#           'formatter': 'default'
#       }},
#       'root': {
#           'level': 'INFO' if app.config['DEBUG'] else 'WARNING',
#           'handlers': ['wsgi']
#       }
#   })
  logging.info('Log information loaded')