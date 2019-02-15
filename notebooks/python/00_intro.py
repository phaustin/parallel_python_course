# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.0.0-rc4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown] {"slideshow": {"slide_type": "slide"}, "toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#00---Introduction" data-toc-modified-id="00---Introduction-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>00 - Introduction</a></span><ul class="toc-item"><li><span><a href="#First-steps" data-toc-modified-id="First-steps-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>First steps</a></span><ul class="toc-item"><li><span><a href="#Installing-python" data-toc-modified-id="Installing-python-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Installing python</a></span></li><li><span><a href="#Installing-extra-dependencies" data-toc-modified-id="Installing-extra-dependencies-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>Installing extra dependencies</a></span></li></ul></li><li><span><a href="#Course-objectives" data-toc-modified-id="Course-objectives-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Course objectives</a></span></li><li><span><a href="#Motivation-(editorial)" data-toc-modified-id="Motivation-(editorial)-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Motivation (editorial)</a></span><ul class="toc-item"><li><span><a href="#Concurrency-vs.-parallelism" data-toc-modified-id="Concurrency-vs.-parallelism-1.3.1"><span class="toc-item-num">1.3.1&nbsp;&nbsp;</span>Concurrency vs. parallelism</a></span></li><li><span><a href="#Threads-and-processes" data-toc-modified-id="Threads-and-processes-1.3.2"><span class="toc-item-num">1.3.2&nbsp;&nbsp;</span>Threads and processes</a></span></li><li><span><a href="#Thread-scheduling" data-toc-modified-id="Thread-scheduling-1.3.3"><span class="toc-item-num">1.3.3&nbsp;&nbsp;</span>Thread scheduling</a></span></li><li><span><a href="#Releasing-the-GIL" data-toc-modified-id="Releasing-the-GIL-1.3.4"><span class="toc-item-num">1.3.4&nbsp;&nbsp;</span>Releasing the GIL</a></span></li></ul></li></ul></li></ul></div>

# %%
from IPython.display import Image

# %% [markdown]
# # 00 - Introduction

# %% [markdown] {"slideshow": {"slide_type": "slide"}}
# ## First steps
#
# **(Note -- this material is under construction and might change significantly between now and June 14)**
#
# ### Installing python
#
# * All the code used in the tutorial can be run on a Windows, Mac, or Linux laptop
#
# * We will use a python distribution called [Anaconda](https://www.anaconda.com/distribution/) to run a series of [Jupyter notebooks](http://jupyter.org/) (you are reading a jupyter notebook now).
#
# * You're definitely encouraged to bring your laptop to the tutorial, please do the following:
#
#   * Download and install Miniconda 3.6 from https://conda.io/miniconda.html on your laptop, accepting all
#     the defaults for the install (I specified an install into a folder named ma36 below):
#   
#   * If you are running on Windows:
#     * Press the &#8862; Win key to open a cmd shell and type:
#            anaconda prompt
#       
#       This should launch a cmd shell that we can use to install other packages
#       
#       To test your installation, type 
#       
#             conda list
#             
#       at the prompt, which should show you a list of installed packages starting with:
#       
#             (base) C:\Users\paust>conda list
#             # packages in environment at C:\Users\paust\ma36:  
#       
#     * If you are running MacOS or Linux, after the install launch a bash terminal. Hopefully
#       when you type:
#
#             conda list
#
#       you will see output that looks like:
#
#
#             % conda list
#             # packages in environment at /Users/phil/mb36:
#             #
#             # Name                    Version                   Build  Channel
#
#
#
# ### Installing extra dependencies
#
# * To install the software required to run the notebooks:
#
#   1.  Download [conda_packages.txt](https://raw.githubusercontent.com/phaustin/parallel_python_course/master/conda_packages.txt) by right-clicking on the link.
#   
#   2. From you cmd or bash terminal, cd to the folder containing that file and do:
#   
#           conda install --file conda_packages.txt
#           
#   3. If this succeeds, then typing the command:
#   
#            python -c 'import numpy;print(numpy.__version__)'
#            
#        should print:
#        
#            1.14.2
#            
#        (or possibly a higher version)
#        
#   4. If you have trouble with these steps, send me a bug report at paustin@eos.ubc.ca and we can iterate. 
#
#

# %% [markdown]
# ## Course objectives
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
#    1.  Using C++ with cffi
# 1. Using [dask](http://dask.pydata.org/en/latest/)/[xarray](http://xarray.pydata.org/en/stable/dask.html) to analyze out-of-core datasets
# 1. Visualizing parallelization with dask
# 1. Setting up a conda-forge environment for parallel computing
#
#
#

# %% [markdown]
# ## Motivation (editorial)
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
#

# %% [markdown]
# ### Concurrency vs. parallelism
#
# [Google says: ](https://www.google.ca/search?q=concurrency+vs.+parallelism&rlz=1C5CHFA_enCA698CA698&oq=conncurrency+vs.+parallel&aqs=chrome.1.69i57j0l5.6167j0j7&sourceid=chrome&ie=UTF-8)

# %% [markdown]
# ### Threads and processes
#
# > From [Wikipedia](https://en.wikipedia.org/wiki/Thread_(computing)):
#
# >> "In computer science, a thread of execution is the smallest sequence of programmed instructions that can be managed independently by a scheduler, which is typically a part of the operating system.[1] The implementation of threads and processes differs between operating systems, but in most cases a thread is a component of a process. Multiple threads can exist within one process, executing concurrently and sharing resources such as memory, while different processes do not share these resources. In particular, the threads of a process share its executable code and the values of its variables at any given time."
#

# %% [markdown]
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

# %% [markdown]
# ### Thread scheduling
#
# If multiple threads are present in a python process, the python intepreter releases the GIL at specified intervals (5 miliseconds default) to allow them to execute:

# %%
Image(filename='images/morreau1.png')  #[Mor2017]

# %% [markdown]
# #### Note that these three threads are taking turns, resulting in a computation that runs slightly slower (because of overhead) than running on a single thread

# %% [markdown]
# ### Releasing the GIL
#
# If the computation running on the thread has released the GIL, then it can run independently of other threads in the process.  Execution of these threads are scheduled by the operating system along with all the other threads and processes on the system.
#
# In particular, basic computation functions in Numpy, like (\__add\__ (+), \__subtract\__ (-) etc. release the GIL, as well as universal math functions like cos, sin etc.

# %%
Image(filename='images/morreau2.png')  #[Morr2017]

# %%
Image(filename='images/morreau3.png') #[Morr2017]
