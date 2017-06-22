
# coding: utf-8

# In[1]:


from IPython.display import Image
import contexttimer
import time
import math
from numba import jit
import multiprocessing
import threading
from joblib import Parallel
import logging


# # Course objectives
# 
# * The objective is to learn how to write shared-memory Python programs that make use of multiple cores on
#   a single node. The tutorial will introduce several python modules that schedule operations and manage
#   data to simplify multiprocessing with Python.
# 
# 1. Benchmarking parallel code
# 1. Understanding the global interpreter lock (GIL)
# 1. Multiprocessing and multithreading with [joblib](https://pythonhosted.org/joblib/)
# 1. Checkpointing/restarting multiprocessor jobs
# 1. Multithreaded file i/o with [zarr](http://zarr.readthedocs.io/en/latest/) and [parquet](https://arrow.apache.org/docs/python/parquet.html)
# 1. Writing extensions that release the GIL:
#    1.  Using [numba](http://numba.pydata.org/)
#    1.  Using [cython](http://cython.org/)
#    1.  Using C++ and [pybind11](http://pybind11.readthedocs.io/en/stable/?badge=stable) with [xtensor-python](https://xtensor-python.readthedocs.io/en/latest/)
# 1. Using [dask](http://dask.pydata.org/en/latest/)/[xarray](http://xarray.pydata.org/en/stable/dask.html) to analyze out-of-core datasets
# 1. Visualizing parallelization with dask
# 1. Setting up a conda-forge environment for parallel computing
# 
# 
# 

# # Motivation (editorial)
# 
# 1. I learned this material by [cargo culting](https://en.wikipedia.org/wiki/Cargo_cult_programming), but my hope is that this set of working examples can shorten the learning curve for newcomers trying to combine Python with C++/C/
# Fortran.  Multiprocessing, multithreading and cross language programming are all in a state of rapid development; these constant changes make it impossible to google a definitive answer about any of these topics.
# 
# 1. I'm presenting my personal opinion about the best way to organize mixed language computer programs so that they:
# 
#    1. Give the same answers each time they are built and run
#    
#    1. Can be easily shared with colleagues, including yourself six months in the future.
#    
#    1. Save time (your time + collaborators' time + machine time). 
#    
# 1. I'll maintain this repository, and test it on Linux, OSX and Windows.  If you hit bugs, I welcome github issues and pull requests, or an emailed questions/examples of problems.
# 
# 1. This is an area of Python programming that is changing/developing on an almost weekly basis.  There's reason to believe that things (meaning the way that we build and deploy multi-language applications) will stabilize over the next year or so. 
# 
# ## References
# 
# * Some history:  https://glyph.twistedmatrix.com/2016/08/python-packaging.html
# 
# * The main Python packaging web site: https://packaging.python.org/
# 
# * Build systems [PEP 517](https://github.com/python/peps/blob/master/pep-0517.txt)
# 
# * Conda: https://conda.io/docs/intro.html
# 

# ## Motivation -- why combine python with C/C++/Fortran?
# 
# 
# * the price of memory and processors continues to decrease
# 
#       Commodity data processor:  [8 cores/16 threads with 16 Gbytes of RAM for $US 2000]             (http://www.titancomputers.com/Titan-X179-Intel-Xeon-E5-V4-Broadwell-EP-Ultra-p/x179.htm)
# 
# * How do we get the most from these increasingly cheap cores?  
# * Python has many strengths, but some limitations.

# ### Threads and processes
# 
# > From [Wikipedia](https://en.wikipedia.org/wiki/Thread_(computing)):
# 
# >> "In computer science, a thread of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system.[1] The implementation of threads and processes differs between operating systems, but in most cases a thread is a component of a process. Multiple threads can exist within one process, executing concurrently and sharing resources such as memory, while different processes do not share these resources. In particular, the threads of a process share its executable code and the values of its variables at any given time."
# 

# #### Threads and processes in Python
# 
# [Reference: Thomas Moreau and Olivier Griesel, PyParis 2017 [Mor2017]](https://tommoral.github.io/pyparis17/#1)
# 
# #### Python global intepreter lock
# 
# 1. Motivation: python objects (lists, dicts, sets, etc.) manage their own memory by storing a counter that keeps track of how many copies of an object are in use.  Memory is reclaimed when that counter goes to zero.
# 
# 1. Having a globally available reference count makes it simple for Python extensions to create, modify and share python objects.
# 
# 1. To avoid memory corruption, a python process will only allow 1 thread at any given moment to run python code.  Any thread that wants to access python objects in that process needs to acquire the global interpreter lock (GIL).
# 
# 1. A python extension written in C, C++ or numba is free to release the GIL, provided it doesn't create, destroy or modify any python objects.  For example: numpy, pandas, scipy.ndimage, scipy.integrate.quadrature all release the GIL
# 
# 1. Many python standard library input/output routines (file reading, networking) also release the GIL
# 
# 1. On the other hand:  hdf5, and therefore h5py and netCDF4, don't release the GIL and are single threaded.
# 
# 1. Python comes with many libraries to manage both processes and threads.
# 

# ### Thread scheduling
# 
# If multiple threads are present in a python process, the python intepreter releases the GIL at specified intervals (5 miliseconds default) to allow them to execute:

# In[4]:


#Image(filename='images/morreau1.png')  #[Mor2017]


# #### Note that these three threads are taking turns, resulting in a computation that runs slightly slower (because of overhead) than running on a single thread

# ### Releasing the GIL
# 
# If the computation running on the thread has released the GIL, then it can run independently of other threads in the process.  Execution of these threads are scheduled by the operating system along with all the other threads and processes on the system.
# 
# In particular, basic computation functions in Numpy, like (\__add\__ (+), \__subtract\__ (-) etc. release the GIL, as well as universal math functions like cos, sin etc.

# In[5]:


#Image(filename='images/morreau2.png')  #[Morr2017]


# In[6]:


#Image(filename='images/morreau3.png') #[Morr2017]

