from .base import BasePlugin


try:
    from fastapi.responses import JSONResponse
except ImportError:
    JSONResponse = None


class FastAPIPlugin(BasePlugin):
    NAME = 'fastapi'
    RESPONSE_CLASS = JSONResponse
    IS_ASYNC = True

    @classmethod
    def make_content(cls, data):
        # yes maybe it looks weird and stupid
        # but it must be so
        return data
