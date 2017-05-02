**Instructor**: Philip Austin (Earth, Ocean and Atmospheric Sciences, UBC)

**Title**: Parallelization in Python 3 with large datasets

**Duration**: 3 hours

**Target audience**: Researchers who develop their own code and consider porting them to GPU

**Level**: intermediate

**Prerequisites**:
* Some familiarity with Jupyter notebooks, Python and numpy at the level of 
  Jake Vanderplas' [Whirlwind tour of Python](https://github.com/jakevdp/WhirlwindTourOfPython/blob/f40b435dea823ad5f094d48d158cc8b8f282e9d5/Index.ipynb)
  or Patrick Wall's [Tuesday introduction to Jupyter](https://github.com/razoumov/summerSchools17/blob/master/ubc/patrick.md)

**Course plan**:

* The objective is to learn how to write shared-memory Python programs that make use of multiple cores on
  a single node. The tutorial will introduce several python modules that schedule operations and manage
  data to simplify multiprocessing with Python.
   

1. Benchmarking parallel code
1. Understanding the global interpreter lock (GIL)
1. Multiprocessing and multithreading with joblib
1. Checkpointing/restarting multiprocessor jobs
1. Writing extensions that release the GIL:
   1.1  Using numba
   1.1  Using cython
   1.1  Using C++ and pybind11
1. Using xarray to analyze out-of-core datasets
1. Using dask and xarray to compute on multiple cores
1. Visualizing parallelization with dask

**Setup requirements**:

* account on bison
* bashrc with python 3.6.1 and g++ 5.2 in path
