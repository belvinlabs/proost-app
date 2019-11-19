import yaml
import logging
import os
import sys
from dotenv import load_dotenv
from logging.config import dictConfig
from git import Repo

service_name = 'default'

try:
    repo = Repo('..')
    branch = repo.active_branch.name
    if branch != 'master':
        service_name = branch.translate({ord(c): "-" for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
except Exception:
    pass

load_dotenv()

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

stream_read = open('src/app.yaml', 'r')

app_yaml = yaml.load(stream_read, Loader)

env_vars = {}
for variable, app_val in app_yaml['env_variables'].items():
  value = os.getenv(variable)
  
  if value:
    logging.info(f'{variable} is set from a local environment variable')
    env_vars[variable] = value
  elif app_val != 'placeholder': 
    logging.info(f'{variable} does not have to be overwritten as it isn\'t a placeholder')
    env_vars[variable] = app_val
  else: 
    logging.error(f'- {variable} environment variable is NOT set. Stopping the process with an error')
    sys.exit(f'Environment variable {variable} is not set')

app_yaml['env_variables'] = env_vars
app_yaml['service'] = service_name

stream_write = open('src/app.yaml', 'w')
yaml.dump(app_yaml, stream_write)

