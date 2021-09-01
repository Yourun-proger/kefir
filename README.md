![](https://img.shields.io/github/v/release/yourun-proger/kefir)
![](https://img.shields.io/github/languages/code-size/yourun-proger/kefir)
![](https://img.shields.io/github/license/yourun-proger/kefir)

# kefir
kefir is a library for convert objects of classes (or models) to dict

this is need for creating some APIs
## Install
```bash
$ cd your_project_dir
$ git clone github.com/yourun-proger/kefir.git
```
## Work
Easy
```py
from pprint import pprint
from kefir.kefir import Kefir
kef = Kefir()
class SomeClass:
  def __init__(self, some_attr):
    self.some_attr = some_attr
class SomeOtherClass:
  def __init__(self, some_attr, some_other_attr):
    self.some_attr = some_attr
    self.some_other_attr = some_other_attr
some = SomeClass('some kefir')
some_dict = kef.dump(some) # {'some_attr': 'some kefir'}
some_other = SomeOtherClass('some other kefir', some)
some_other_dict = kef.dump(some_other)
pprint(some_other_dict)
>>> {'some_attr': 'some other kefir', 'some_other_attr': {'some_attr': 'some kefir'}}
```
real example
```py
from flask import Flask, jsonify, request
from my_models import db, User, Order #NOTE: today kefir does not support all db relations :p
from kefir.kefir import Kefir
app = Flask(__name__)
kef = Kefir(
              session=db.session,
              shorcuts={'users':'user'},
              objects={'users':User}
           )
@app.get('/orders/<int:order_id>')
def order_view(order_id):
  order = Order.query.get(order_id) # Order(id=4,adress='some', bill=123, user_id=42)
  order_dict = kef.dump(order)  # {'id':4, 'adress':'some','bill':123,'user':{'id':42,'name':'Kefir', 'email':'kefir_mail@notreal.uncom'}}
  return jsonify(order)
if __name__ == '__main__:
  app.run()
```
## Reqs
this support python 3.6+ (may be 3.5-)
## About
i created this only for fun

*But i true think this project become big and very cool ( 11.08.2021 )*
## FAQ
q: why it is needed, be cause we have marshmallow, pydantic e t.c.

a: i want to be a part of "e t.c." + this is very cool for small APIs

q: Release on PyPi?

a: in progress. Please waiting)
## Contibuting
today this project is very raw and when it has no 1.0 version this isnt't needed to pr or issues

but you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Conclusion
get star if you like this, please)

*Thanks for reading and have a good day!*
