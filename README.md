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
from kefir import kefir
class SomeClass:
  def __init__(self, some_attr):
    self.some_attr = some_attr
class SomeOtherClass:
  def __init__(self, some_attr, some_other_attr):
    self.some_attr = some_attr
    self.some_other_attr = some_other_attr
some = SomeClass('some kefir')
some_dict = kefir.dump_to_dict(some) # {'some_attr': 'some kefir'}
some_other = SomeOtherClass('some other kefir', some)
some_other_dict = kefir.dump_to_dict(some_other)
pprint(some_other_dict)
>>> {'some_attr': 'some other kefir', 'some_other_attr': {'some_attr': 'some kefir'}}
```
real example
```py
from flask import Flask, jsonify, request
from my_models import SomeModel #NOTE: today kefir does not support relations
from kefir import kefir
app = Flask(__name__)
@app.get('/all_models')
def check():
  all_models = SomeModel.query.all()
  all_models_dict = kefir.dump_to_dict(all_models, one=False)
  return jsonify(all_models_dict)
@app.get('/one_model/<int:model_id>')
def check_one(model_id):
  one_model = SomeModel.query.get(model_id)
  one_model_dict = kefir.dump_to_dict(one_model)
  return jsonify(one_model_dict)
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
