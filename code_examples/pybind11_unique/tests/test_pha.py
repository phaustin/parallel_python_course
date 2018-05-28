import cpp_make_unique as uniq
import numpy as np

type_dict={'double':(np.float64,uniq.make_unique_double),
           'float':(np.float32,uniq.make_unique_float),
           'int64_t':(np.int64,uniq.make_unique_int64),
           'int32_t':(np.int32,uniq.make_unique_int32)}


for type_key,value in type_dict.items():
    print(f'testing {type_key}')
    np_type,the_fun = value
    in_vec_test=np.array([0, 5, 5, 1, 2,2,2, 3, 4,4,4,4,4, 5],dtype=np_type)
    num_in = in_vec_test.size
    print(f'original vector: {in_vec_test}')
    out_n=the_fun(in_vec_test,num_in)
    in_vec=in_vec_test[0:out_n]
    print('after call: ',in_vec)
    del in_vec_test
    del in_vec
    
    

