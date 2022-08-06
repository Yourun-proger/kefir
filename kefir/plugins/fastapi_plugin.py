from .base import BasePlugin

from fastapi.responses import JSONResponse


class FastAPIPlugin(BasePlugin):
    IS_ASYNC = True

    @staticmethod
    def make_response(content):
        return JSONResponse(content)
