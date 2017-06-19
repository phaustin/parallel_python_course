**Instructor**: Philip Austin (Earth, Ocean and Atmospheric Sciences, UBC)

**Title**: Parallelization in Python 3 with large datasets

**Duration**: 3 hours

**Target audience**: Researchers interested in Python programming on multiple core machines.

**Level**: Intermediate

**Prerequisites**:
* Some familiarity with Jupyter notebooks, Python and numpy at the level of 
  Jake Vanderplas' [Whirlwind tour of Python](https://github.com/jakevdp/WhirlwindTourOfPython/blob/f40b435dea823ad5f094d48d158cc8b8f282e9d5/Index.ipynb)
  or this week's  [Tuesday introduction to Jupyter by Patrick Wall](https://github.com/razoumov/summerSchools17/blob/master/ubc/patrick.md)

**Course plan**:

* The objective is to learn how to write shared-memory Python programs that make use of multiple cores on
  a single node. The tutorial will introduce several python modules that schedule operations and manage
  data to simplify multiprocessing with Python.

1. Benchmarking parallel code
1. Understanding the global interpreter lock (GIL)
1. Multiprocessing and multithreading with [joblib](https://pythonhosted.org/joblib/)
1. Checkpointing/restarting multiprocessor jobs
1. Multithreaded file i/o with [zarr](http://zarr.readthedocs.io/en/latest/) and [parquet](https://arrow.apache.org/docs/python/parquet.html)
1. Writing extensions that release the GIL:
   1.  Using [numba](http://numba.pydata.org/)
   1.  Using [cython](http://cython.org/)
   1.  Using C++ and [pybind11](http://pybind11.readthedocs.io/en/stable/?badge=stable) with [xtensor-python](https://xtensor-python.readthedocs.io/en/latest/)
1. Using [dask](http://dask.pydata.org/en/latest/)/[xarray](http://xarray.pydata.org/en/stable/dask.html) to analyze out-of-core datasets
1. Visualizing parallelization with dask
1. Setting up a conda-forge environment for parallel computing

**Setup requirements**:

### For remote access to Westgrid

* A laptop with the [x2go client](http://wiki.x2go.org/doku.php/download:start) installed
* An account on grex
* .bashrc which adds python 3.6.1 and g++ 5.2 to the PATH

### For your own laptop

I'd encourage you do a local python install on your laptop, to make sure we don't
don't get hit by bandwidth limitations or competition for cpus on grex nodes.

We will need python 3.6 from conda-forge.  To get it:

1. Download miniconda 3.6 from https://conda.io/miniconda.html

1. When prompted, set the install directory as something like /Users/phil/mini36,
with the install for just yourself, but ignore the installer warning and make this your default
python.  To reverse that decision it is easy to edit either your .bashrc/.bash_profile (for OSX)
or your PATH environmental varialbe (for Windows 10) and give higher priority to some other python executable.  It will make the following step easier, however if this conda-forge python is your default for the class and the install below

1. Set conda-forge as your default repository and upgrade your python by doing the following.
   Open a bash terminal (OSX) or a cmd shell (Windows) and type:

         conda config --prepend channels conda-forge

   followed by:

         conda update --all

1. Once the update completes, copy the contents of https://github.com/phaustin/parallel_python_course/blob/master/conda_packages.txt
into a local file named conda_packages.txt and install those packages by typing:

        conda install --file conda_packages.txt


### If the install fails

The odds of this going smoothly for everyone are obviously close to zero.  If all else fails you can follow along using a browser to point to my html files, and get the jupyter notebooks working at your leisure after class.   All the notebooks we work with during the tutorial will be available in the github repository, and from my bison account.  Feel free to email me at paustin@eoas.ubc.ca with any questions.


