![](https://img.shields.io/github/v/release/yourun-proger/kefir)
![](https://img.shields.io/github/languages/code-size/yourun-proger/kefir)
![](https://img.shields.io/github/license/yourun-proger/kefir)

# kefir
kefir is a library for convert SQLAlchemy models or complex objects to dict
## Install
```bash
$ git clone https://github.com/Yourun-proger/kefir.git
$ cd kefir
$ pip install -e .
```
**Before installation, it is advisable [to create and activate a virtual environment](https://github.com/Yourun-proger/kefir/wiki/Docs#create-and-activate-virtual-env) !!!**
## Example
```py
from pprint import pprint
from kefir import Kefir
kef = Kefir()
class A:
  def __init__(self, some_attr):
    self.a_attr = some_attr
class B:
  def __init__(self, some_attr, some_a_object):
    self.b_attr = some_attr
    self.b_a_object = some_a_object
a_object = A('kefir')
b_object = B(42, a_object)
pprint(kef.dump(b_object))
>>> {'b_attr': 42, 'b_a_object': {'a_attr': 'kefir'}}
```
## Docs
See [this](https://github.com/Yourun-proger/kefir/wiki/Docs)

## Requirements
It is hard to say. It all depends on the source codebase and legacy code.
But it definitely works for:
* *python **3.8.2***
* *sqlalchemy **1.4.27***

because it is my configurations xD
## About
i created this only for fun and because i tired to write Schemas

*But i true think this project become big and very cool ( 11.08.2021 )*
## Contributing
today this project is very raw and when it has no 1.0 version this isnt't needed to pr or issues

but you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Conclusion
GIve a ✨ for this project if you ❤ this, please)

*Thanks for reading and have a good day!*
