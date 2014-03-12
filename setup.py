import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as infile:
        return infile.read()


setup(
    name="django-typetable",
    version="0.1",
    description="Database-backed enumerations for Django.",
    license="LGPL3",
    url="https://github.com/leo-the-manic/django-typetables",
    packages=['typetable'],
    long_description=read('README.rst'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: LGPL3 License",
    ],
)
