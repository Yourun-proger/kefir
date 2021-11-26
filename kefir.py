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

    def __init__(self, session=None, objects={}, rels={}, ignore={}, shorcuts={}):
        self.session = session  # SQLAlhcemy session
        self.objects = objects  # tablename -> Class; {'users':User} for example. this is needed for relations
        self.rels = rels  # some relations of tables. Example: rels={'users':['orders']}. users table is main in rels with orders
        self.ignore = ignore
        self.shorcuts = shorcuts

    def _is_custom_class(self, obj):
        return not (
                isinstance(obj, int) or \
                isinstance(obj, str) or \
                isinstance(obj, bool) or \
                isinstance(obj, dict) or \
                isinstance(obj, float)
        )

    def _is_foreign_key(self, table, col):
        dct = {}
        for i in table.columns:
            rels = []
            if i.foreign_keys:
                for j in i.foreign_keys:
                    rels.append((j._column_tokens[1], j._column_tokens[2]))

            dct[i.name] = rels

        return dct[col]

    def dump(self, obj, ignore=()):
        if isinstance(obj, list):
            lst = []
            for i in obj:
                lst.append(self.dump(i))
            return lst
        else:
            obj_type = 'class'
            if "<class 'sqlalchemy.ext.declarative.api.Model'>" in list(map(str, type(obj).mro())):  # looks bad =_=
                obj_type = 'model'

            if obj_type == 'class':
                dct = {}
                try:
                    obj.__slots__
                    has_slots = True
                except AttributeError:
                    has_slots = False
                if has_slots:
                    for key in obj.__slots__:
                        if self._is_custom_class(getattr(obj, key)):
                            dct[key] = self.dump(getattr(obj, key))
                        else:
                            dct[key] = getattr(obj, key)
                else:
                    for key, value in obj.__dict__.items():
                        if not key.startswith('_'):
                            if self._is_custom_class(value):
                                dct[key] = self.dump(value)
                            else:
                                dct[key] = value
                return dct
            elif obj_type == 'model':
                dct = {}
                done = []
                table = obj.metadata.tables[obj.__tablename__]
                cols = [str(col[len(obj.__tablename__) + 1:]) for col in list(map(str, table.columns))]
                for col in cols:
                    if self._is_foreign_key(table, col):
                        for i in self._is_foreign_key(table, col):
                            if i[0] not in ignore and  i[0] not in self.ignore.get(obj.__tablename__,[]):
                                sql = 'SELECT * FROM ' + i[0] + ' WHERE ' + i[1] + ' = ' + '"' + str(
                                    getattr(obj, col)) + '"' + ';'
                                data = self.session.execute(sql).cursor.fetchall()
                                cols = self.session.execute(sql).__dict__['_metadata'].keys
                                if len(data) == 1:
                                    dct[self.shorcuts.get(i[0], i[0])] = dict(zip(cols, data[0]))
                                else:
                                    dct[self.shorcuts.get(i[0], i[0])] = [dict(zip(cols, i)) for i in data]

                    dct[col] = getattr(obj, col)
                if self.rels.get(obj.__tablename__):
                    for i in self.rels[obj.__tablename__]:
                        obj_arg = list(obj.__dict__['_sa_instance_state'].__dict__ \
                                           ['manager'].__dict__['local_attrs'][i].__dict__ \
                                           ['comparator'].__dict__['_parententity'].__dict__ \
                                           ['_init_properties'][i].__dict__ \
                                           ['synchronize_pairs'][0][1].__dict__ \
                                           ['foreign_keys'])[0].__dict__['_column_tokens'][2]

                        rel_obj_arg = list(obj.__dict__['_sa_instance_state'].__dict__['manager'].__dict__ \
                                               ['local_attrs'][i].__dict__['comparator'].__dict__ \
                                               ['_parententity'].__dict__['_init_properties'][i].__dict__ \
                                               ['synchronize_pairs'][0][1].__dict__['foreign_keys'])[0].__dict__ \
                                          ['parent'].__dict__['_key_label'][len(i) + 1:]
                        sql = 'SELECT * FROM ' + i + ' WHERE ' + rel_obj_arg + ' = ' + '"' + str(
                            getattr(obj, obj_arg)) + '"' + ';'
                        data = self.session.execute(sql).fetchall()
                        cols = self.session.execute(sql).__dict__['_metadata'].keys
                        if len(data) == 1:
                            dct[self.shorcuts.get(i, i)] = self.dump(self.objects[i].query.get(data[0]),
                                                                     [obj.__tablename__])
                        else:
                            dct[self.shorcuts.get(i, i)] = [
                                self.dump(self.objects[i].query.get(j[0]), [obj.__tablename__]) for j in data]
                return dct
    
    def dump_route(self, method):
        """
        Special decorator for dumping returned value of your Flask view-function
        Today - ONLY FOR FLASK!
        easy example:
        @app.get('/users/<int:user_id>')
        @kef.dump_route
        def f(user_id):
            return User.query.get(user_id)
        WARNING:
        `dump_route` must be entre the `route` decorator and view function.
        that has similar sense with this:
        -> https://flask-caching.readthedocs.io/en/latest/#caching-view-functions
        """
        @wraps(method)
        def dump_response(*args, **kwargs):
            content = self.dump(method(*args, **kwargs))
            if Response is not None:
                response = Response(dumps(content), mimetype='application/json')
            else:
                raise PleaseInstallException('If you want to use `dump_route`, please install Flask!')
            return response
        return dump_response

class PleaseInstallException(Exception):...
