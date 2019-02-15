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
# <div class="toc"><ul class="toc-item"><li><span><a href="#05---Using-conda-to-manage-C++-libraries" data-toc-modified-id="05---Using-conda-to-manage-C++-libraries-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>05 - Using conda to manage C++ libraries</a></span></li><li><span><a href="#Using-conda-to-manage-python-libraries" data-toc-modified-id="Using-conda-to-manage-python-libraries-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Using conda to manage python libraries</a></span><ul class="toc-item"><li><span><a href="#Accessing-the-functions-from-python-using-CFFI" data-toc-modified-id="Accessing-the-functions-from-python-using-CFFI-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Accessing the functions from python using CFFI</a></span><ul class="toc-item"><li><span><a href="#Running-this-in-a-threadpool" data-toc-modified-id="Running-this-in-a-threadpool-2.1.1"><span class="toc-item-num">2.1.1&nbsp;&nbsp;</span>Running this in a threadpool</a></span></li></ul></li></ul></li></ul></div>

# %% [markdown]
# # 05 - Using conda to manage C++ libraries
#
# The [cffi_funs](https://github.com/phaustin/parallel_python_course/tree/master/code_examples/cffi_funs) folder shows how to set up a C++ file so that it compiled with [cmake](http://preshing.com/20170511/how-to-build-a-cmake-based-project/) and also [here](http://preshing.com/20170522/learn-cmakes-scripting-language-in-15-minutes/)
#
# The folder contains [these files](https://github.com/phaustin/parallel_python_course/blob/master/code_examples/cffi_funs/Readme_cffi_funs.rst)
#
# **Demo**
#
# Show how to build a conda archive with:
#
#     conda build .
#     
# and then upload it to your [Anaconda channel](https://anaconda.org/phaustin/dashboard)
#
# Where it can be installed into a conda environment with:
#
#     conda install -c phaustin cffi_funs

# %% [markdown]
# # Using conda to manage python libraries
#
# The [cffi_practice](https://github.com/phaustin/parallel_python_course/tree/master/code_examples/cffi_practice)
# folder shows how to install a simple python project using conda and [setuptools](http://setuptools.readthedocs.io/en/latest/setuptools.html)
#
# **Demo**
#
# Show how to build and upload cffi_practice to my conda channel
#
# The purpose of this module is to provide one function:
#
#     cffi_practice.get_paths()
#     
# That can be used to locate the library and header from cff_funs
#
# The get_paths function is defined in this package in the [__init__.py](https://github.com/phaustin/parallel_python_course/blob/master/code_examples/cffi_practice/cffi_practice/__init__.py) module.
#
# Try:
#
#     conda install cff_practice -c phaustin
#     
# Then:
#
#     python -c 'import cffi_practice;print(cffi_practice.get_paths())'
#     
# Which should output something like:
#
#     {'libfile': '/Users/phil/mini36/lib/libcffi_funs.so', 'libdir': '/Users/phil/mini36/lib', 'includedir': '/Users/phil/mini36/include'}

# %% [markdown]
# ## Accessing the functions from python using CFFI
#
# The [C foreign function interface](https://cffi.readthedocs.io/en/latest/overview.html) provides a way to call the cffi_funs from python
#
# Here is an example that exposes the get_thread_id and get_proces_id functions from the cffi_fun package

# %%
from cffi import FFI
from joblib import Parallel
from cffi_practice import get_paths
#
#  locate the library
#
lib_so_file=get_paths()['libfile']
ffi=FFI()
ffi.cdef("""
    void get_thread_id(char *thread_id);
    void get_process_id(char *process_id);
""")
#
#  open the library file
#
lib = ffi.dlopen(lib_so_file)
print('found these functions in module: ',dir(lib))
#
# create a 25 character C array to hold the ouput
#
arg_thread = ffi.new("char[]",25)  #(C++)
#
# # copy the bytes into arg_thread  (C++)
#
lib.get_thread_id(arg_thread)  
#
# get the bytes into a python byte object
#
out_thread=ffi.string(arg_thread)  #C++ to python
#
# turn the bytes into a utf-8 string
#
str_out=out_thread.decode('utf-8')  #python
#
# print it out
#
print(f"Here is the thread id in hex: -{str_out}-")
#
# repeat for the process
#
arg_process = ffi.new("char[]",25) 
lib.get_process_id(arg_process)
out_process=ffi.string(arg_process)
str_out=out_process.decode('utf-8')
print(f"here is the process ide in base 10: -{str_out}-")

# %% [markdown]
# ### Running this in a threadpool
#
# The following script uses joblib to create 10 jobs to call the cffi functions in parallel, returning
# the pointers to the character array and convertingthem to python strings.

# %%
nprocs=10
arg_list=[]
fun_list=[]
dict_list=[]
for i in range(nprocs):
    fun_list.append(lib.get_thread_id)
    result_var=ffi.new("char[]",25)
    arg_list.append(result_var)
    dict_list.append({})
ptr_list=[[ffi.cast("char*",item)] for item in arg_list]
jobs=list(zip(fun_list,ptr_list,dict_list))
print(f'here are the pointers to hold the ids: {ptr_list}\n')
with Parallel(n_jobs=nprocs,backend='threading') as parallel:
    parallel(jobs)
print('here are the thread ids')
for item in ptr_list:
    out_thread=ffi.string(item[0]).decode('utf-8')
    print('thread id: ',out_thread)

# %%
