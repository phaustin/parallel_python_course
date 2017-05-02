**Instructor**: Philip Austin (Earth, Ocean and Atmospheric Sciences, UBC)

**Title**: Parallelization in Python 3 with large datasets

**Duration**: 3 hours

**Target audience**: Researchers interested in Python programming on multiple core machines.

**Level**: Intermediate

**Prerequisites**:
* Some familiarity with Jupyter notebooks, Python and numpy at the level of 
  Jake Vanderplas' [Whirlwind tour of Python](https://github.com/jakevdp/WhirlwindTourOfPython/blob/f40b435dea823ad5f094d48d158cc8b8f282e9d5/Index.ipynb)
  or this week's  [Tuesday introduction to Jupyter by Patrick Wall](https://github.com/razoumov/summerSchools17/blob/master/ubc/patrick.md)

**Course plan**:

* The objective is to learn how to write shared-memory Python programs that make use of multiple cores on
  a single node. The tutorial will introduce several python modules that schedule operations and manage
  data to simplify multiprocessing with Python.

1. Benchmarking parallel code
1. Understanding the global interpreter lock (GIL)
1. Multiprocessing and multithreading with joblib
1. Checkpointing/restarting multiprocessor jobs
1. Writing extensions that release the GIL:
   1.  Using numba
   1.  Using cython
   1.  Using C++ and pybind11
1. Using xarray to analyze out-of-core datasets
1. Using dask and xarray to compute on multiple cores
1. Visualizing parallelization with dask
1. Setting up a conda-forge environment for parallel computing

**Setup requirements**:

* A laptop with the [x2go client](http://wiki.x2go.org/doku.php/download:start) installed
* An account on bison
* .bashrc which adds python 3.6.1 and g++ 5.2 to the PATH
