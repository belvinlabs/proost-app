import logging

from utils.app import jsonify, dump_json
from utils.enums import APIErrorTypes
from uuid import uuid1


class APIError(Exception):

    def __init__(self, http_code, error_type_key, message, error_id=None):
        self.http_code = http_code
        self.error_id = error_id or str(uuid1())
        self.error_type_key = APIErrorTypes(error_type_key)
        self.message = message

    def as_dict(self):
        return {
            'http_code': self.http_code,
            'error_id': self.error_id,
            'error_type_key': self.error_type_key.name,
            'message': self.message
        }

    def __str__(self):
        error_json = dump_json(self.as_dict())
        return f'{self.__class__.__name__}: \n' \
               f'{error_json}'

    def as_response(self):
        logging.warn(self)
        return jsonify({
           '__error': self.as_dict()
        }), self.http_code
