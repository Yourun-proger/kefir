from setuptools import setup
from kefir import __version__


setup(
    name="kefir",
    version=__version__,
    url="https://github.com/Yourun-proger/kefir/",
    license="MIT",
    author="Yourun-proger",
    description="Easy (de)serialization of SQLAlchemy models and complex objects",
    packages=["kefir"],
    platforms="any",
    zip_safe=False,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
