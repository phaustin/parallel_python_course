
# coding: utf-8

# In[1]:


import numpy as np
import zarr
import time
import datetime
import pytz
from zarr.util import human_readable_size
import dask
import dask.array as da
from dask.diagnostics import Profiler, ResourceProfiler, CacheProfiler
from dask.diagnostics.profile_visualize import visualize


# # Using dask and zarr for multithreaded input/output

# * Many python programmers use [hdf5](https://support.hdfgroup.org/HDF5/) through either the [h5py](http://www.h5py.org/) or [pytables](http://www.pytables.org/) modules to store large dense arrays.  One drawback of the hdf5 implementation is that it is basically **single-threaded**, that is only one core can read or write to a dataset at any one time.  Multithreading makes data compression much more attractive, because data sections can be decompressing/compressing simultaneouly while the data is read/written.
# 
# ## zarr
# 
# * [zarr](http://zarr.readthedocs.io/en/latest/?badge=latest) keeps the h5py interface (which is similar to numpy's), but allows different choices for file compression and is fully multithreaded.  See [Alistair Miles original blog entry](http://alimanfoo.github.io/2016/05/16/cpu-blues.html) for a discussion of the motivation behind zarr.
# 
# ## dask
# 
# * [dask](http://dask.pydata.org/en/latest/) is a Python library that implements lazy data structures (array, dataframe, bag) and a clever thread/process scheduler.  It integrates with zarr to allow calculations on datasets that don't fit into core memory, either in a single node or across a cluster.

# ### Example, write and read zarr arrays using multiple threads

# ### Create 230 Mbytes of  fake data

# In[2]:


wvel_data = np.random.normal(2000, 1000, size=[8000,7500]).astype(np.float32)
human_readable_size(wvel_data.nbytes)


# ### Copy to a zarr file on disk, using multiple threads

# In[3]:


item='disk1_data'
store = zarr.DirectoryStore(item)
group=zarr.hierarchy.group(store=store,overwrite=True,synchronizer=zarr.ThreadSynchronizer())
the_var='wvel'
out_zarr1=group.zeros(the_var,shape=wvel_data.shape,dtype=wvel_data.dtype,chunks=[2000,7500])
out_zarr1[...]=wvel_data[...]


# ### Add some attributes

# In[4]:


now=datetime.datetime.now(pytz.UTC)
timestamp= int(now.strftime('%s'))
out_zarr1.attrs['history']='written for practice'
out_zarr1.attrs['creation_date']=str(now)
out_zarr1.attrs['gmt_timestap']=timestamp
out_zarr1


# ### Create an array of zeros -- note that compression shrinks it from 230 Mbytes to 321 bytes

# In[5]:


a2 = np.zeros([8000,7500],dtype=np.float32)
item='disk2_data'
store = zarr.DirectoryStore(item)
group=zarr.hierarchy.group(store=store,overwrite=True,synchronizer=zarr.ThreadSynchronizer())
the_var='wvel'
out_zarr2=group.zeros(the_var,shape=a2.shape,dtype=a2.dtype,chunks=[2000,7500])
out_zarr2


# ### copy input to output using chunks

# In[6]:


item='disk2_data'
store = zarr.DirectoryStore(item)
group=zarr.hierarchy.group(store=store,overwrite=True,synchronizer=zarr.ThreadSynchronizer())
the_var='wvel'
out_zarr=group.empty(the_var,shape=wvel_data.shape,dtype=wvel_data.dtype,chunks=[2000,7500])
out_zarr2[...]=out_zarr1[...]
out_zarr2


# ### Create a dask array from a zarr disk file

# In[7]:


da_input = da.from_array(out_zarr2, chunks=out_zarr1.chunks)
da_input


# ### The following calculation uses numpy, so it releases the GIL

# In[8]:


result=(da_input**2. + da_input**3.).mean(axis=0)
result


# ### Note that result hasn't been computed yet
# 
# Here is a graph of how the calculation will be split among 4 threads

# In[12]:


# from dask.dot import dot_graph
# dot_graph(out.dask)


# ### Now do the calculation

# In[10]:


with Profiler() as prof, ResourceProfiler(dt=0.1) as rprof,              CacheProfiler() as cprof:
    answer = result.compute()

print('here is rprof: ',rprof)

# Visualize the cpu, memory and cache for the 4 threads

# In[11]:


#visualize([prof, rprof,cprof], min_border_top=15, min_border_bottom=15)


# ### You can evaluate your own functions on dask arrays
# 
# If your functons release the GIL, you can get multithreaded computation using [dask.delayed](http://dask.pydata.org/en/latest/delayed.html)
