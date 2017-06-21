* Example project for a pure python module

* Contents

  * setup.py

    -- module that setuptools calls to construct the package

  * cffi_practice

    - __init__.py -- definds function cffi_practice.get_paths() that return the location
      of the cffi_funs.h and libcffi_funs.so files

  * recipe

    - conda recipe

To install
++++++++++

1. In the cffi_practice directory, do::

      conda build .

1. This should a line  that looks something like::

      anaconda upload /Users/phil/mtest/conda-bld/noarch/cffi_practice-0.1-py_0.tar.bz2

1. Either follow that instruction and upload to your anaconda account, or install to your conda environment with::

      conda install /Users/phil/mtest/conda-bld/noarch/cffi_practice-0.1-py_0.tar.bz2

