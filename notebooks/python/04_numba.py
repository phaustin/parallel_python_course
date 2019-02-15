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
# <div class="toc"><ul class="toc-item"><li><span><a href="#04---Using-numba-to-release-the-GIL" data-toc-modified-id="04---Using-numba-to-release-the-GIL-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>04 - Using numba to release the GIL</a></span><ul class="toc-item"><li><ul class="toc-item"><li><span><a href="#Timing-python-code" data-toc-modified-id="Timing-python-code-1.0.1"><span class="toc-item-num">1.0.1&nbsp;&nbsp;</span>Timing python code</a></span></li><li><span><a href="#Now-try-this-with-numba" data-toc-modified-id="Now-try-this-with-numba-1.0.2"><span class="toc-item-num">1.0.2&nbsp;&nbsp;</span>Now try this with numba</a></span></li><li><span><a href="#Make-two-identical-functions:-one-that-releases-and-one-that-holds-the-GIL" data-toc-modified-id="Make-two-identical-functions:-one-that-releases-and-one-that-holds-the-GIL-1.0.3"><span class="toc-item-num">1.0.3&nbsp;&nbsp;</span>Make two identical functions: one that releases and one that holds the GIL</a></span></li><li><span><a href="#now-time-wait_loop_withgil" data-toc-modified-id="now-time-wait_loop_withgil-1.0.4"><span class="toc-item-num">1.0.4&nbsp;&nbsp;</span>now time wait_loop_withgil</a></span></li><li><span><a href="#not-bad,-but-we're-only-using-one-core" data-toc-modified-id="not-bad,-but-we're-only-using-one-core-1.0.5"><span class="toc-item-num">1.0.5&nbsp;&nbsp;</span>not bad, but we're only using one core</a></span></li></ul></li></ul></li></ul></div>

# %% [markdown]
#     pip install contexttimer
#     conda install numba
#     conda install joblib

# %%
from IPython.display import Image
import contexttimer
import time
import math
from numba import jit
from joblib import Parallel
import logging


# %% [markdown]
# # 04 - Using numba to release the GIL

# %% [markdown]
# ### Timing python code
#
#
# One easy way to tell whether you are utilizing multiple cores is to track the wall clock time measured by [time.perf_counter](https://docs.python.org/3/library/time.html#time.perf_counter) against the total cpu time used by all threads meausred with [time.process_time](https://docs.python.org/3/library/time.html#time.process_time)
#
# I'll organize these two timers using the [contexttimer](https://github.com/brouberol/contexttimer) module.

# %% [markdown]
# To install, in a shell window type:
#
#      pip install contexttimer

# %% [markdown]
# #### Define a function that does a lot of computation

# %%
def wait_loop(n):
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
# #### now time it with pure python

# %%
nloops=200
with contexttimer.Timer(time.perf_counter) as pure_wall:
    with contexttimer.Timer(time.process_time) as pure_cpu:
        result=wait_loop(nloops)
print(f'pure python wall time {pure_wall.elapsed} and cpu time {pure_cpu.elapsed}')


# %% [markdown]
# ### Now try this with numba
#
# Numba is a just in time compiler that can turn a subset of python into machine code using the llvm compiler.
#
# Reference:  [Numba documentation](http://numba.pydata.org/numba-doc/dev/index.html)

# %% [markdown]
# ### Make two identical functions: one that releases and one that holds the GIL

# %%
@jit('float64(int64)', nopython=True, nogil=True)
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
@jit('float64(int64)', nopython=True, nogil=False)
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
# ### now time wait\_loop\_withgil

# %%
nloops=500
with contexttimer.Timer(time.perf_counter) as numba_wall:
    with contexttimer.Timer(time.process_time) as numba_cpu:
        result=wait_loop_withgil(nloops)
print(f'numba wall time {numba_wall.elapsed} and cpu time {numba_cpu.elapsed}')
print(f"numba speed-up factor {(pure_wall.elapsed - numba_wall.elapsed)/numba_wall.elapsed}")

# %% [markdown]
# ### not bad, but we're only using one core
