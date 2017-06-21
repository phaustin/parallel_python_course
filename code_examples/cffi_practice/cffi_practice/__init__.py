# import version for use by setup.py
from ._version import version_info, __version__  # noqa: F401 imported but unused
from pathlib import Path
from pip import locations

def get_paths(*args, **kwargs):
    binpath=Path(locations.distutils_scheme('cffi_practice', *args, **kwargs)['scripts'])
    libfile=Path.joinpath(binpath.parent,Path('lib/libcffi_funs.so'))
    libdir=Path.joinpath(binpath.parent,Path('lib'))
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
    return out_dict

