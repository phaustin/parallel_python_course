
# coding: utf-8

# In[2]:


from IPython.display import Image
import contexttimer
import time
import math
from numba import jit
import multiprocessing
import threading
from joblib import Parallel
import logging


# ## Creating a thread pool with joblib
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

# ### Our functions from the numba notebook 

# In[3]:


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


# In[13]:


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


# ### Setup logging so we can know what process and thread we are running

# In[6]:


logging.basicConfig(level=logging.DEBUG,
                    format='%(message)s %(threadName)s %(processName)s',
                    )

def find_ids():
    logging.debug('debug logging: ')


# ### Create two functions, one to print thread and process ids, and one to run the wait_for loop
# 
# * Important point -- the logging module is **threadsafe**
# 
# * Submit 6 jobs queued on 3 processors

# In[11]:


njobs=6
nprocs=3
thread_id_jobs =[(find_ids,[],{}) for i in range(nprocs)]
nloops=1250
calc_jobs=[(wait_loop_nogil,[nloops],{}) for i in range(njobs)]
print(calc_jobs)


# In[15]:


with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='threading') as parallel:
            parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')


# * Each job was run on a different thread but in the same process
# 
# * Note that the cpu time is larger than the wall time, confirming that we've release the GIL.
# 

# ### Now repeat this holding the GIL

# In[14]:


calc_jobs=[(wait_loop_withgil,[nloops],{}) for i in range(njobs)]
with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='threading') as parallel:
            parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')


# ** Note that the speed is the same as if we ran on a single CPU **

# ### Now repeat with processes instead of threads

# In[16]:


calc_jobs=[(wait_loop_withgil,[nloops],{}) for i in range(njobs)]
with contexttimer.Timer(time.perf_counter) as wall:
    with contexttimer.Timer(time.process_time) as cpu:
        with Parallel(n_jobs=nprocs,backend='multiprocessing') as parallel:
            parallel(thread_id_jobs)
            results=parallel(calc_jobs)
        print(results)
print(f'wall time {wall.elapsed} and cpu time {cpu.elapsed}')


# ** how do you explain the tiny cpu time? **

# ###  Summary
# 
# 1.  For simple functions without Python code, Numba can release the GIL and you can get the benefit of multiple threads
# 
# 1. The joblib library can be used to queue dozens of jobs onto a specified number of processes or threads
# 
# 1. A process pool can execute pure python routines, but all data has to be copied to and from each process.

# In[ ]:




