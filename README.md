[![CI](https://github.com/Yourun-proger/kefir/actions/workflows/python-package.yml/badge.svg)](https://github.com/Yourun-proger/kefir/actions/workflows/python-package.yml)
![](https://img.shields.io/github/v/release/yourun-proger/kefir)
![](https://img.shields.io/github/languages/code-size/yourun-proger/kefir)
![](https://img.shields.io/github/license/yourun-proger/kefir)

# kefir
kefir is a framework for convert SQLAlchemy models or complex objects to dict
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

class A:
  def __init__(self, some_attr):
    self.attr = some_attr

class B:
  def __init__(self, some_attr, some_a_object):
    self.attr = some_attr
    self.a_object = some_a_object

a_object = A('kefir')
b_object = B(42, a_object)

kef = Kefir()
pprint(kef.dump(b_object))
>>> {'attr': 42, 'a_object': {'attr': 'kefir'}}
```
## Docs
See [this](https://github.com/Yourun-proger/kefir/wiki/Docs)

## Requirements
Kefir supports python 3.7+
## About
I created this only for fun and because i tired to write Schemas

*But i true think this project become big and very cool ( 11.08.2021 )*
## Contributing
Open for issues as minimal feedback needed!

Closed for pull requests as still raw

Also you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Support Project
Give a ✨ for this project if you ❤ this, please)

*Have a good day!*
