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
# <div class="toc"><ul class="toc-item"><li><span><a href="#06---Using-conda-to-manage-C++-libraries-with-pybind11" data-toc-modified-id="06---Using-conda-to-manage-C++-libraries-with-pybind11-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>06 - Using conda to manage C++ libraries with pybind11</a></span></li></ul></div>

# %% [markdown]
# # 06 - Using conda to manage C++ libraries with pybind11
#
#
# The [pybind11_demo](https://github.com/phaustin/parallel_python_course/tree/master/code_examples/pybind11_demo) folder shows how to use [pybind11](http://pybind11.readthedocs.io/en/stable/?badge=stable) and [xtensor-python](https://xtensor-python.readthedocs.io/en/latest/) to export numerical C++ functions and classes to python.
#
# This is similar to cffi, but contains many more convenience functions to make it easier to work with numpy arrays and python lists, dicts, etc. in C++ while releasing the GIL.
#
# Here is the [filelist](https://github.com/phaustin/parallel_python_course/blob/master/code_examples/pybind11_demo/Readme_pybind11_demo.rst)
#
#
#
#
# **Demo**
#
# Show how to build a conda archive for the thread_tools pbackage
#
#     conda build .
#     
# and then upload it to your [Anaconda channel](https://anaconda.org/phaustin/dashboard)
#
# Where it can be installed into a conda environment with:
#
#     conda install -c phaustin thread_tools
#     
# If successful, running:
#
#     python test_wait.py
#     
# should produce output like this:
#
#     pybind11 wall time 2.0149485040456057 and cpu time 1.968194
#     
#     

# %%
