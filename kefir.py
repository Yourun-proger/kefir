"""
Kefir main file
"""

from functools import wraps
from json import dumps

try:
    from flask import Response
except ImportError:
    Response = None


class Kefir:
    def __init__(self):
        ...  # place for future work

    def dump(self, obj, ignore=None):
        if isinstance(obj, list):
            lst = []
            for item in obj:
                lst.append(self.dump(item))
            return lst
        dct = {}
        if obj.__dict__.get('_sa_instance_state'):
            for k, v in obj.__dict__['_sa_instance_state'].__dict__['manager'].__dict__['local_attrs'].items():
                item = getattr(obj,k)
                if item is not ignore:
                    if isinstance(item, (int, str, bool, dict, float)):
                        dct[k] = item
                    else:
                        if isinstance(item, list):
                            dct[k] = [self.dump(i, obj) for i in item]
                        else:
                            dct[k] = self.dump(item, obj)
        else:
            if hasattr(obj, '__slots__'):
                for k in obj.__slots__:
                    if isinstance(getattr(obj,k), (int, str, bool, dict, float)):
                        dct[k] = getattr(obj, k)
                    else:
                        dct[k] = self.dump(getattr(obj, k))
            for k, v in obj.__dict__.items():
                if not k.startswith('_'):
                    if isinstance(v, (int, str, bool, dict, float)):
                        dct[k] = v
                    else:
                        dct[k] = self.dump(v)

        return dct
    
    def dump_route(self, method):
        """
        Special decorator for dumping returned value of your Flask view-function
        ONLY FOR FLASK!!!
        easy example:
        @app.get('/users/<int:user_id>')
        @kef.dump_route
        def f(user_id):
            return User.query.get(user_id)
        WARNING:
        `dump_route` must be enter the `route` decorator and view function.
        that has similar sense with this:
        -> https://flask-caching.readthedocs.io/en/latest/#caching-view-functions
        """
        @wraps(method)
        def dump_response(*args, **kwargs):
            content = self.dump(method(*args, **kwargs))
            if Response is None:
                raise PleaseInstallException('If you want to use `dump_route`, please install Flask!')
            response = Response(dumps(content), mimetype='application/json')
            return response
        return dump_response

class PleaseInstallException(Exception):...
