from dask.distributed import Client
from multiprocessing.pool import ThreadPool
import dask
import dask.array as da
import numpy as np
# pool = ThreadPool(4)
# dask.set_options(pool=pool)
# client=Client()
import zarr, glob
zarr_files=sorted(glob.glob("bomex*zarr"))
print(zarr_files)

in_dict={}
for timestep,item in enumerate(zarr_files):
    store = zarr.DirectoryStore(item)
    the_vars=['PP', 'QN', 'QV', 'TABS', 'TR01', 'U','V', 'W']
    for a_var in the_vars:
        group=zarr.hierarchy.open_group(store=store, mode='r', synchronizer=zarr.ThreadSynchronizer())
        in_dict[(timestep,a_var)]=group[a_var]
        
out_dict={}

item='newout'
store = zarr.DirectoryStore(item)
group=zarr.hierarchy.group(store=store,overwrite=True,synchronizer=zarr.ThreadSynchronizer())
ntimesteps=len(zarr_files)
for a_var in the_vars:
    out_dict[a_var]=group.empty(a_var,shape=[ntimesteps,128,256,256],chunks=[2,128,256,256],synchronizer=zarr.ThreadSynchronizer(),dtype=np.float32)
    for timestep in range(ntimesteps):
        out_dict[a_var][timestep,:,:,:] = in_dict[(timestep,a_var)][0,:,:,:]

print(out_dict)

item='newout'
store = zarr.DirectoryStore(item)
group=zarr.hierarchy.open_group(store=store, mode='r', synchronizer=zarr.ThreadSynchronizer())
print(group)
print(group['PP'].shape)

# vars=['PP', 'QN', 'QV', 'TABS', 'TR01', 'U','V', 'W']
# out_name='testit'
# store = zarr.DirectoryStore(out_name)
# the_group=zarr.hierarchy.group(store=store,overwrite=True,
#                                     synchronizer=zarr.ThreadSynchronizer())
# disk_out=the_group.zeros('big_out',shape=[1,1,128,256,256],
#                          chunks=[128,256,256],dtype='float32',
#                          compressor=zarr.Blosc(cname='zstd', clevel=1, shuffle=2))
# disk_out[0,0,0,0,:]=np.arange(256)
# print(dir(the_group))
# help(the_group.empty)
# disk_out=the_group.empty('big_out',mode='w',shape=[8,5,128,256,256],
#                          chunks=[128,256,256],dtype='float32',
#                          )


# for timestep,zfile in enumerate(zarr_files[:2]):
#     root = zarr.open_group(zfile, mode='r')
#     print(root)
#     for index,the_var in enumerate(vars[:1]):
#         test=root[the_var][0,:,:,:]
#         print(type(test),test.shape)
#         disk_out[index,timestep,:,:,:]=test[...]
        
