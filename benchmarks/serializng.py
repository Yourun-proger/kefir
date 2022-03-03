from timeit import timeit
from kefir import Kefir, Repr
from marshmallow import Schema, fields


class Note:
    def __init__(self, id, title, desc):
        self.id = id
        self.title = title
        self.desc = desc


class NoteSchema(Schema):
    id = fields.Integer()
    title = fields.Str()
    description = fields.Str(attribute="desc")


class NoteRepr(Repr):
    names_map = {"desc": "description"}


note_schema = NoteSchema(many=True)

notes = [
    Note(id=i, title=f"title #{i}", desc=f"very long desc {i} {i*10} {i+1}")
    for i in range(10)
]

kef = Kefir({Note:NoteRepr})


def do_kef():
    return kef.dump(notes)


def do_marshmallow():
    return note_schema.dump(notes)


print("kefir:         ", timeit("do()", globals={"do": do_kef}, number=100000))  # 3.4900028
print("marshmallow:   ", timeit("do()", globals={"do": do_marshmallow}, number=100000))  # 6.742087300000001
