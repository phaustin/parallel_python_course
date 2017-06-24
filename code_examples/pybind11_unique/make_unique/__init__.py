# import version for use by setup.py
from ._version import version_info, __version__  # noqa: F401 imported but unused
from pathlib import Path
from pip import locations

def get_paths(*args, **kwargs):
    binpath=Path(locations.distutils_scheme('make_unique', *args, **kwargs)['scripts'])
    libdir=Path.joinpath(binpath.parent,Path('lib'))
    #
    # find either libcffi_funs.so or libcffi_funs.dll
    #
    library=list(libdir.glob('libmake_unique.*'))
    if len(library) > 1:
        raise ImportError('found more than one libmake_uniqu library')
    try:
        libfile=library[0]
    except IndexError:
        libfile=Path('libmake_unique')
    includedir=Path.joinpath(binpath.parent,Path('include'))
    for the_path in [libfile, libdir, includedir]:
        if not the_path.exists():
            print(f"couldn't find {str(the_path)}. Did you install make_unique?")
            out_dict=None
            break
    else:
        out_dict=dict(libfile=str(libfile),libdir=str(libdir),includedir=str(includedir))
    return out_dict


signatures={'float64':'uint64_t make_unique_double(double *in_vec, uint64_t n);',
            'float32' :'uint64_t make_unique_float(float *in_vec, uint64_t n);',
            'int64'   :'uint64_t make_unique_int64(int64_t *in_vec, uint64_t n);',
            'int32'   :'uint64_t make_unique_int32(int32_t *in_vec, uint64_t n);'}
