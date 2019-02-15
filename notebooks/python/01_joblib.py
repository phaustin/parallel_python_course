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

# %% [markdown] {"toc": true}
# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#01---Introduction-to-joblib" data-toc-modified-id="01---Introduction-to-joblib-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>01 - Introduction to joblib</a></span><ul class="toc-item"><li><span><a href="#Creating-a-process-or-thread-pool-with-joblib" data-toc-modified-id="Creating-a-process-or-thread-pool-with-joblib-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Creating a process or thread pool with joblib</a></span><ul class="toc-item"><li><span><a href="#Running-a-threadsafe-function" data-toc-modified-id="Running-a-threadsafe-function-1.1.1"><span class="toc-item-num">1.1.1&nbsp;&nbsp;</span>Running a threadsafe function</a></span></li><li><span><a href="#Setup-logging-so-we-can-know-what-process-and-thread-we-are-running" data-toc-modified-id="Setup-logging-so-we-can-know-what-process-and-thread-we-are-running-1.1.2"><span class="toc-item-num">1.1.2&nbsp;&nbsp;</span>Setup logging so we can know what process and thread we are running</a></span></li><li><span><a href="#Create-two-functions,-one-to-print-thread-and-process-ids,-and-one-to-run-the-wait_for-loop" data-toc-modified-id="Create-two-functions,-one-to-print-thread-and-process-ids,-and-one-to-run-the-wait_for-loop-1.1.3"><span class="toc-item-num">1.1.3&nbsp;&nbsp;</span>Create two functions, one to print thread and process ids, and one to run the wait_for loop</a></span></li><li><span><a href="#Now-repeat-this-holding-the-GIL" data-toc-modified-id="Now-repeat-this-holding-the-GIL-1.1.4"><span class="toc-item-num">1.1.4&nbsp;&nbsp;</span>Now repeat this holding the GIL</a></span></li><li><span><a href="#Now-repeat-with-processes-instead-of-threads" data-toc-modified-id="Now-repeat-with-processes-instead-of-threads-1.1.5"><span class="toc-item-num">1.1.5&nbsp;&nbsp;</span>Now repeat with processes instead of threads</a></span></li><li><span><a href="#Summary" data-toc-modified-id="Summary-1.1.6"><span class="toc-item-num">1.1.6&nbsp;&nbsp;</span>Summary</a></span></li></ul></li></ul></li></ul></div>

# %% [markdown]
# # 01 - Introduction to joblib
#
# This notebook shows how to use joblib to execute jobs on multiple threads or processes

# %% [markdown]
# need to install two packages
#
#     pip install contextttimer
#
#     conda install joblib

# %%
from IPython.display import Image
import contexttimer
import time
import math
from numba import jit
import multiprocessing
import threading
from joblib import Parallel
import logging


# %% [markdown]
# ## Creating a process or thread pool with joblib
#
# [joblib](https://pythonhosted.org/joblib/index.html) Provides the best way to run naively parallel jobs on multiple threads or processes in python.
#
# * It integrates seamlessly with [dask](http://distributed.readthedocs.io/en/latest/joblib.html)
#   and [scikit-learn](http://scikit-learn.org/stable/modules/model_persistence.html)
#   
# * It is undergoing rapid development: e.g. [loky](https://github.com/tomMoral/loky)
#
# * To use it, create a Parallel object that runs a list of functions, where each function is part of a tuple that specifies the arguments and keywords (if any)
#

# %% [markdown]
# ### Running a threadsafe function 

# %%
@jit('float64(int64)', nopython=True, nogil=True)  #release the GIL!
def wait_loop_nogil(n):
    """
    Function under test.
    """
    for m in range(n):
        for l in range(m):
            for j in range(l):
                for i in range(j):
                    i=i+4
                    out=math.sqrt(i)
                    out=out**2.
    return out


# %%
@jit('float64(int64)', nopython=True, nogil=False) #hold the GIL
def wait_loop_withgil(n):
    """
    Function under test.
    """
    for m in range(n):
        for l in range(m):
            for j in range(l):
                for i in range(j):
                    i=i+4
                    out=math.sqrt(i)
                    out=out**2.
    return out


# %% [markdown]
# ### Setup logging so we can know what process and thread we are running

# %%
logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s %(threadName)s %(processName)s',
                    )

def find_ids():
    logging.debug('debug logging: ')


# %% [markdown]
# ### Create two functions, one to print thread and process ids, and one to run the wait_for loop
#
# * Important point -- the logging module is **threadsafe**
#
# * Submit 6 jobs queued on 3 processors

# %%
njobs=12
nprocs=3
thread_id_jobs =[(find_ids,[],{}) for i in range(nprocs)]
nloops=1250
calc_jobs=[(wait_loop_nogil,[nloops],{}) for i in range(njobs)]
print(calc_jobs)

# %%
with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='threading') as parallel:
            #parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')

# %% [markdown]
# * Each job was run on a different thread but in the same process
#
# * Note that the cpu time is larger than the wall time, confirming that we've release the GIL.
#

# %% [markdown]
# ### Now repeat this holding the GIL
#
# Create a new set of jobs that hold the GIL

# %%
calc_jobs=[(wait_loop_withgil,[nloops],{}) for i in range(njobs)]
with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='threading') as parallel:
            #parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')

# %% [markdown]
# ** Note that the speed is the same as if we ran on a single CPU **

# %% [markdown]
# ### Now repeat with processes instead of threads

# %%
calc_jobs=[(wait_loop_withgil,[nloops],{}) for i in range(njobs)]
with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='multiprocessing') as parallel:
            #parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')

# %% [markdown]
# ** how do you explain the tiny cpu time? **

# %% [markdown]
# ###  Summary
#
# 1.  For simple functions without Python code, Numba can release the GIL and you can get the benefit of multiple threads
#
# 1. The joblib library can be used to queue dozens of jobs onto a specified number of processes or threads
#
# 1. A process pool can execute pure python routines, but all data has to be copied to and from each process.

# %%
