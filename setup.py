from setuptools import setup
from kefir import __version__


setup(
    name='kefir',
    version=__version__,
    url='https://github.com/yourun-proger/kefir/',
    license='MIT',
    author='Yourun-Proger',
    description='convert SQLAlchemy models or custom-class objects to python dict',
    py_modules=['kefir'],
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
