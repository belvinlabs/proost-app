import threading
import requests
import os
import json
from utils.app import app
from google.cloud import tasks_v2
from google.protobuf import timestamp_pb2


def start_local_task(url, data):
    requests.post(url, json=data)


def create_task(req, relative_url, data):
    if not os.getenv('GOOGLE_CLOUD_PROJECT'):
        url = f'{req.scheme}://{req.host}{relative_url}'
        x = threading.Thread(target=start_local_task, daemon=True, 
                             args=[url, data])
        x.start()
    else:
        client = tasks_v2.CloudTasksClient()
        project = os.getenv('GOOGLE_CLOUD_PROJECT')
        queue = app.config['CLOUD_TASK_QUEUE']
        location = 'us-central1'
        payload = json.dumps(data)

        parent = client.queue_path(project, location, queue)

        task = {
            'app_engine_http_request': {  # Specify the type of request.
                'http_method': 'POST',
                'relative_uri': f'{relative_url}',
                'headers': {
                    'Content-Type': "application/json",
                },
                'app_engine_routing': {
                    'service': os.getenv('GAE_SERVICE'),
                    'version': os.getenv('GAE_VERSION')
                }
            }
        }
        if payload is not None:
            # The API expects a payload of type bytes.
            converted_payload = payload.encode()

            # Add the payload to the request.
            task['app_engine_http_request']['body'] = converted_payload

        response = client.create_task(parent, task)
