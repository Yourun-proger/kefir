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
**Before installation, it is advisable to create and activate a virtual environment !!!**
## Example
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
## Docs
See [this](https://github.com/Yourun-proger/kefir/wiki/Docs) page

## Requirements
this support python 3.6+
## About
i created this only for fun

*But i true think this project become big and very cool ( 11.08.2021 )*
## Contributing
today this project is very raw and when it has no 1.0 version this isnt't needed to pr or issues

but you can give me some feedback on [discusssion](https://github.com/Yourun-proger/kefir/discussions/2)
## Conclusion
get star if you like this, please)

*Thanks for reading and have a good day!*
