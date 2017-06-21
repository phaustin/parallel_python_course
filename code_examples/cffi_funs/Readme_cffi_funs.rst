* Example project compiling a set of C++ functions into a shared library

* Contents

  * CMakeLists.txt

    -- CMake file that produces libcffi_funs.so

  * cffi_headers/c_lib.h

    - include file for libcffi_funs declarations

  * src/c_lib.cpp

    - function definitions

To install
++++++++++

1. In the cffi_funs directory, do::

      conda build .

1. This should a line  that looks something like::

      anaconda upload /Users/phil/mtest/conda-bld/osx-64/cffi_funs-dev-0.tar.bz2

1. Either follow that instruction and upload to your anaconda account, or install to your conda environment with::

      conda install /Users/phil/mtest/conda-bld/osx-64/cffi_funs-dev-0.tar.bz2

