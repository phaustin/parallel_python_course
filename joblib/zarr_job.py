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


vars=['PP', 'QN', 'QV', 'TABS', 'TR01', 'U','V', 'W']
disk_out=zarr.open_array('big_out.zarr',mode='w',shape=[8,5,128,256,256],
                         chunks=[128,256,256],dtype='float32',fill_value=0,synchronizer=zarr.ThreadSynchronizer())
print(disk_out)
for timestep,zfile in enumerate(zarr_files[:2]):
    root = zarr.open_group(zfile, mode='r')
    print(root)
    for index,the_var in enumerate(vars[:1]):
        test=root[the_var][0,:,:,:]
        print(type(test),test.shape)
        disk_out[index,timestep,:,:,:]=test[...]
        
