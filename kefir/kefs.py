import functools
import json

from kefir.base import BaseKefir
from kefir.exceptions import PleaseInstallException

try:
    from flask import Response as FlaskResponse
except ImportError:
    FlaskResponse = None

try:
    from fastapi.responses import JSONResponse as FastAPIResponse
except ImportError:
    FastAPIResponse = None


class SyncKefir(BaseKefir):
    def __init__(self, represents, datetime_format, used):
        super().__init__(represents, datetime_format, used)

    def dump_route(self, view_func):
        """
        Special decorator for dumping returned value of your Flask or FastAPI view-function
        Simple example:
        @app.route('/users/<int:user_id>')
        @kef.dump_route
        def user_view(user_id):
            return User.query.get(user_id)
        WARNING:
        `dump_route` must be between the `route` decorator and view function
        """

        @functools.wraps(view_func)
        def dump_response(*args, **kwargs):
            content = self.dump(view_func(*args, **kwargs))
            if self.used.lower() == "flask":
                if FlaskResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install Flask!"
                    )
                response = FlaskResponse(
                    json.dumps(content), mimetype="application/json"
                )
                return response
            elif self.used.lower() == "fastapi":
                if FastAPIResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install FastAPI!"
                    )
                response = FastAPIResponse(content)
                return response
            else:
                raise ValueError('`used` arg can be only "flask" or "fastapi" string')

        return dump_response


class AsyncKefir(BaseKefir):
    def __init__(self, represents, datetime_format, used):
        super().__init__(represents, datetime_format, used)

    def dump_route(self, view_func):
        # The functions are very similar... Am I breaking DRY?
        # I guess I'll take Uncle Bob's advice and leave it as it is...
        @functools.wraps(view_func)
        async def dump_response(*args, **kwargs):
            content = self.dump(await view_func(*args, **kwargs))
            if self.used.lower() == "flask":
                if FlaskResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install Flask!"
                    )
                response = FlaskResponse(json.dump(content), mimetype="application/json")
                return response
            elif self.used.lower() == "fastapi":
                if FastAPIResponse is None:
                    raise PleaseInstallException(
                        "If you want to use `dump_route`, please install FastAPI!"
                    )
                response = FastAPIResponse(content)
                return response
            else:
                raise ValueError('`used` arg can be only "flask" or "fastapi" string')
        return dump_response
