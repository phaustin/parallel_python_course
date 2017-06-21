#!/usr/bin/env python

# Setup script for PyPI; use CMakeFile.txt to build extension modules

from setuptools import setup
from cffi_practice import __version__


setup(
    name='cffi_practice',
    version=__version__,
    packages=['cffi_practice'],
    classifiers=[
        'License :: OSI Approved :: BSD License'
    ],
    keywords='C++11, Python bindings',
    long_description="""pybind11""")

