from .base import BasePlugin

import json


try:
    from flask import Response
except ImportError:
    Response = None


class FlaskPlugin(BasePlugin):
    NAME = 'flask'
    RESPONSE_CLASS = Response
    ADDITIONAL_KWARGS = {'mimetype': 'application/json'}

    @classmethod
    def make_content(cls, data):
        return json.dumps(data)
