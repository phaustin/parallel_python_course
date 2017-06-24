from cffi import FFI
from make_unique import get_paths, signatures
import numpy as np
#
#  locate the library
#
lib_so_file=get_paths()['libfile']
ffi=FFI()
sig_text =  """
             {float64:s}
             {float32:s}
             {int64:s}
             {int32:s}
            """.format_map(signatures)
print(sig_text)
ffi.cdef(sig_text)
#
#  open the library file
#
lib = ffi.dlopen(lib_so_file)
print('found these functions in module: ',dir(lib))

make_unique_double=lib.make_unique_double

type_dict=dict(double=np.float64,float=np.float32,int=np.int64)    
in_vec=np.array([0, 5, 5, 1, 2,2,2, 3, 4,4,4,4,4, 5],dtype=np.float64)
invec_ptr = ffi.cast("double *", in_vec.ctypes.data)
invec_len=in_vec.size

type_dict={'double':(np.float64,lib.make_unique_double),
           'float':(np.float32,lib.make_unique_float),
           'int64_t':(np.int64,lib.make_unique_int64),
           'int32_t':(np.int32,lib.make_unique_int32)}

in_vec=np.array([0, 5, 5, 1, 2,2,2, 3, 4,4,4,4,4, 5])
print(f'original vector: {in_vec}')
for type_key,value in type_dict.items():
    print(f'testing {type_key}')
    np_type,the_fun = value
    in_vec=np.array([0, 5, 5, 1, 2,2,2, 3, 4,4,4,4,4, 5],dtype=np_type)
    cast_string=f"{type_key} *"
    invec_ptr = ffi.cast(cast_string, in_vec.ctypes.data)
    out_n=the_fun(invec_ptr,invec_len)
    in_vec=in_vec[0:out_n]
    print('after call: ',in_vec)

