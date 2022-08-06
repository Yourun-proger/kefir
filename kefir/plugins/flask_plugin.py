from .base import BasePlugin

import json
from flask import Response


class Flask(BasePlugin):
    IS_ASYNC = False

    @staticmethod
    def make_response(content):
        return Response(json.dumps(content), mimetype='application/json')
