# import version for use by setup.py
from ._version import version_info, __version__  # noqa: F401 imported but unused
from pathlib import Path
import pdb
import os
import pdb

def get_paths(*args, **kwargs):
    binpath=Path(os.environ['CONDA_PREFIX'])
<<<<<<< HEAD
    libfile= binpath / Path('lib/libcffi_funs.so')
    libdir= binpath / Path('lib')
    pdb.set_trace()
    #
    # find either libcffi_funs.so or libcffi_funs.dll
    #
    library=list(libdir.glob('libcffi_funs.*'))
    
    if len(library) > 1:
        raise ImportError('found more than one libcffi_funs library')
    try:
        libfile=library[0]
    except IndexError:
        libfile=Path('libcffi_funs')
    includedir=Path.joinpath(binpath.parent,Path('include'))
    for the_path in [libfile, libdir, includedir]:
        if not the_path.exists():
            print(f"couldn't find {str(the_path)}. Did you install cffi_funs?")
            out_dict=None
            break
    else:
        out_dict=dict(libfile=str(libfile),libdir=str(libdir),includedir=str(includedir))
=======
    libfile= binpath/ Path('lib/libcffi_funs.so')
    libdir= binpath / Path('lib')
    includedir = binpath / Path('include')
    out_dict=dict(libfile=str(libfile),libdir=str(libdir),includedir=str(includedir))
>>>>>>> checkpoint
    return out_dict

