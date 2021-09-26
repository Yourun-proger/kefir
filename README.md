![](https://img.shields.io/github/v/release/yourun-proger/kefir)
![](https://img.shields.io/github/languages/code-size/yourun-proger/kefir)
![](https://img.shields.io/github/license/yourun-proger/kefir)

# kefir
kefir is a library for convert objects of classes (or models) to dict
## Install
```bash
$ cd your_project_dir
$ git clone https://github.com/Yourun-proger/kefir.git
$ pip install -e .
```
Or
```bash
$ pip install git+https://github.com/Yourun-proger/kefir.git
```
**Before installation, it is advisable to create and activate a virtual environment !!!**
## Work
Easy
```py
from pprint import pprint
from kefir import Kefir
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
from my_models import db, User, Order #NOTE: today kefir does not support nested relations and many2may probable too :|
from kefir import Kefir
app = Flask(__name__)
kef = Kefir(
              session=db.session,
              shorcuts={'users':'user'},
              objects={'users':User},
              rels={'users':['orders']}
           )
@app.get('/orders/<int:order_id>/')
def order_view(order_id):
  order = Order.query.get(order_id) # Order(id=4,adress='some', bill=123, user_id=42)
  order_dict = kef.dump(order)  # {'id':4, 'adress':'some','bill':123,'user':{'id':42,'name':'Kefir', 'email':'kefir_mail@notreal.uncom'}}
  return jsonify(order)
@app.get('/users/<int:user_id>/')
def user_view(user_id):
  user = User.query.get(user_id)  #User(id=42, name='Kefir', email='kefir_mail@notreal.uncom')
  user_dict = kef.dump(user)  # {'id':42,'name':'Kefir','email':'kefir_mail@notreal.uncom','orders'=[{'id':4,'adress':'some','bill':123}, {'id': 101,'adress':'another','bill':321}]}
  return jsonify(user_dict)
  
if __name__ == '__main__':
  app.run()
```
Also see this example:
```py
from dataclasses import dataclass
from pprint import pprint
from kefir import Kefir

class A:
    def __init__(self, attr, attr2):
        self.attr = attr
        self.attr2 = attr
class B:
    def __init__(self, attr, attr2, a):
        self.attr = attr
        self.attr2 = attr2
        self.a = a
class AWithSlots:
    __slots__ = ['attr', 'attr2', 'b']
    def __init__(self, attr, attr2, b):
        self.attr = attr
        self.attr2 = attr2
        self.b = b
@dataclass
class BDataClass:
    attr:str
    attr2:int
    c:AWithSlots

kef = Kefir()
a = A('kefir', 0.2)
b = B('is', 7, a)
c = AWithSlots('the', 42, b)
d = BDataClass('best!', 10101, c)

pprint(kef.dump(a))
pprint(kef.dump(b))
pprint(kef.dump(c))
pprint(kef.dump(d))
"""
Output:
{'attr': 'kefir', 'attr2': 'kefir'}
{'a': {'attr': 'kefir', 'attr2': 'kefir'}, 'attr': 'is', 'attr2': 7}
{'attr': 'the',
 'attr2': 42,
 'b': {'a': {'attr': 'kefir', 'attr2': 'kefir'}, 'attr': 'is', 'attr2': 7}}
{'attr': 'best!',
 'attr2': 10101,
 'c': {'attr': 'the',
       'attr2': 42,
       'b': {'a': {'attr': 'kefir', 'attr2': 'kefir'},
             'attr': 'is',
             'attr2': 7}}}
"""
```
## Requirements
this support python 3.6+
## About
i created this only for fun

*But i true think this project become big and very cool ( 11.08.2021 )*
## FAQ
q: why it is needed, be cause we have marshmallow, pydantic e t.c.

a: The trick is that you don't need to write Schema or add in your project more deps if you do small app or you need only for `dump` and `load` in future ;) methods

q: Release on PyPi?

a: in progress. Please waiting)
## Contributing
today this project is very raw and when it has no 1.0 version this isnt't needed to pr or issues

but you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Conclusion
get star if you like this, please)

*Thanks for reading and have a good day!*
