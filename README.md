[![CI](https://github.com/Yourun-proger/kefir/actions/workflows/python-package.yml/badge.svg)](https://github.com/Yourun-proger/kefir/actions/workflows/python-package.yml)
![](https://img.shields.io/github/v/release/yourun-proger/kefir)
![](https://img.shields.io/github/languages/code-size/yourun-proger/kefir)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![](https://img.shields.io/github/license/yourun-proger/kefir)

# kefir
kefir is a framework for convert SQLAlchemy models or complex objects to dict and back
## Install
Just type:
```bash
$ pip install -e git+https://github.com/Yourun-proger/kefir.git#egg=kefir
```
Or like this if you want to do some changes:
```bash
$ git clone https://github.com/Yourun-proger/kefir.git
$ cd kefir
$ pip install -e .
```
**Before installation, it is advisable [to create and activate a virtual environment](https://github.com/Yourun-proger/kefir/wiki/Docs#create-and-activate-virtual-env) !!!**
## Example
```py
from kefir import Kefir, Repr

class A:
  def __init__(self, some_attr):
    self.attr = some_attr

class B:
  def __init__(self, some_attr, some_a_object):
    self.attr = some_attr
    self.a_object = some_a_object

class BRepr(Repr):
    loads = {'a_object': A}

a_object = A('kefir')
b_object = B(42, a_object)

raw_data = {'attr': 123, 'a_object': {'attr': 456}}

kef = Kefir(represents={B:BRepr})
new_b_object = kef.load(raw_data, B)  # same as B(123, A(456))
raw_b_object = kef.dump(b_object)
print(new_b_object)
print(raw_b_object)
>>> <__main__.B object at some_hash>
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

Now open for pull requests! See [kefir devguide](https://github.com/Yourun-proger/kefir/wiki/Developer-Guide).

Also you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Support Project
Give a ✨ for this project if you ❤ this, please)

*Have a good day!*
