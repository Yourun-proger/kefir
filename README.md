# kefir
keifr is a library for convert objects of classes (or models) to dict
this is need for creating some APIs
## Install
```bash
$ cd your_project_dir
$ git clone github.com/yourun-proger/kefir.git
```
## Work
so easy)
```py
from pprint import pprint
from kefir import kefir
class SomeCoolClass:
  def __init__(self, some_attr):
    self.some_attr = some_attr
some = SomeCoolClass('keifr')
some_dict = kefir.dump_to_dict(some)
pprint(some_dict)
>>> {'some_attr': 'keifr'}
```
more real example
```py
from flask import Flask, jsonify, request
from my_models import SomeModel
from kefir import kefir
app = Flask(__name__)
@app.get('/mymodels_please')
def check():
  all_models = SomeModel.query.all()
  all_models_dict = kefir.dump_to_dict(all_models, one=False)
  return jsonify(all_models_dict)
@app.get('/onlyonemodel')
def check_one():
  model_id = int(request.args('id', 0))
  one_model = SomeModel.query.get(model_id)
  one_model_dict = kefir.dump_to_dict(one_model)
  return jsonify(one_model_dict)
if __name__ == '__main__:
  app.run()
```
## Reqs
this support python 3.6+ (may be -)
## About
i created this with ***COFFE*** (not real) standard
COFFE - **C**reated **O**nly **F**or **F**un **E**ducation
## FAQ
q: why it is needed, be cause we have marshmallow, pydantic e t.c.

a: i want to be a part of "e t.c." + this is very cool for small APIs

q: Releas on PyPi?

a: in progress. Please waiting)
## Contibuting
please no contribue (we have no 0.0.1 version)
## Conclusion
get star if u like this, please)

Thanks for reading and have a good day!
