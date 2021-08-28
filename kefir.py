class Kefir:
    def __init__(self, session=None, shorcuts={}, ignore=[], objects={}):
        self.session = session  # SQLAlhcemy session
        self.shorcuts = shorcuts # for change name of tables to your choose
        # Example
        # print(kef.dump(order))
        # {'id':1, 'items': [...], 'users': {'id':84, 'name':'Kefir'}}
        # this looks bad, because only one user can be owner of order (in your API!)
        # kef = Kefir(db.session, {'users':'user'})
        # print(kef.dump(order))
        # {'id':1, 'items': [...], 'user': {'id':84, 'name':'Kefir'}}
        # Good!
        self.ignore = ignore # tables for ignoring
        self.objects = objects # tablename -> Class; {'users':User} for example. this is needed for relations
    
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
    
    def dump(self, obj):
        if isinstance(obj , list):
            lst = []
            for i in obj:
                lst.append(self.dump(i))
            return lst
        else:
            obj_type = 'class'
            if "<class 'sqlalchemy.ext.declarative.api.Model'>" in list(map(str, type(obj).mro())):
                obj_type = 'model'
            
            if obj_type == 'class':
                dct = {}
                for key, value in obj.__dict__.items():
                    if not key.startswith('_'):
                        if self._is_custom_class(value):
                            dct[key] = self.dump(value)
                        else:
                            dct[key] = value
                return dct
            elif obj_type == 'model':
                dct = {}
                table = obj.metadata.tables[obj.__tablename__]
                cols = [str(col[len(obj.__tablename__)+1:]) for col in list(map(str, table.columns))]
                for col in cols:
                    if self._is_foreign_key(table, col):
                        for i in  self._is_foreign_key(table, col):
                           if i[0] not in self.ignore:
                               sql = 'SELECT * FROM '+ i[0]  + ' WHERE ' + i[1] + '= ' + '"' + str(getattr(obj, col)) + '"'
                               data = self.session.execute(sql).cursor.fetchone()
                               new_obj = self.objects[i[0]].query.get(data[0])
                               dct[self.shorcuts.get(i[0], i[0])] = self.dump(new_obj)
                    else:
                        dct[col] = getattr(obj, col)
                return dct
