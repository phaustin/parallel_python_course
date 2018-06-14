"""
  westgrid.data_read 
  __________________

  downloads a file named filename from the atsc500 downloads directory
  and save it as a local file with the same name. 

  to run from the command line::

    python -m a500.utils.data_read photon_data.csv

    
  to run from a python script::

    from westgrid.data_read import download
    download('photon_data.csv')

  or::

    from westgrid.data_read import download
    root="https://oceandata.sci.gsfc.nasa.gov/cgi/getfile"
    filename="A20162092016216.L3m_8D_PAR_par_9km.nc"
    download(filename,root=root)

"""
import argparse
import requests
from pathlib import Path
import shutil

class NoDataException(Exception):
    pass

def download(filename,root='https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads'):
    """
    copy file filename from http://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads to 
    the local directory.  If local file exists, report file size and quit.

    
    Parameters
    ----------

    filename: string
      name of file to fetch from 

    Returns
    -------

    Side effect: Creates a copy of that file in the local directory
    """
    url = '{}/{}'.format(root,filename)
    print('trying {}'.format(url))
    filepath = Path('./{}'.format(filename))
    print('writing to: {}'.format(str(filepath)))
    if filepath.exists():
        the_size = filepath.stat().st_size
        print(('\n{} already exists\n'
               'and is {} bytes\n'
               'will not overwrite\n').format(filename,the_size))
        return None

    tempfile = str(filepath) + '_tmp'
    temppath = Path(tempfile)
    try:
        with open(tempfile, 'wb') as localfile:
            temppath=Path(tempfile)
            print('writing temporary file {}'.format(temppath))
            response = requests.get(url, stream=True)
            #
            # treat a 'Not Found' response differently, since you want to catch
            # this and possibly continue with a new file
            #
            if not response.ok:
                if response.reason=='Not Found':
                    the_msg='requests.get() returned "Not found" with filename {}'.format(filename)
                    raise NoDataException(the_msg)
                else:
                    #
                    # if we get some other response, raise a general exception
                    #
                    the_msg='requests.get() returned {} with filename {}'.format(response.reason,filename)
                    raise RuntimeError(the_msg)
                    #
                # clean up the temporary file
                #
            for block in response.iter_content(1024):
                if not block:
                    break
                localfile.write(block)
        the_size=temppath.stat().st_size
        print('downloaded {}\nsize = {}'.format(filename,the_size))
        shutil.move(str(temppath),str(filepath))
        if the_size < 10.e3:
            print('Warning -- your file is tiny (smaller than 10 Kbyte)\nDid something go wrong?')
    except NoDataException as e:
        print(e)
        print('clean up: removing {}'.format(temppath))
        temppath.unlink()
    return None


def make_parser():
    """
    set up the command line arguments needed to call the program
    """
    linebreaks = argparse.RawTextHelpFormatter
    parser = argparse.ArgumentParser(
        formatter_class=linebreaks, description=__doc__.lstrip())
    parser.add_argument('filename', type=str, help='name of file to download')
    parser.add_argument("--root", default="https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads",
                        help="root of url, detaults to https://clouds.eos.ubc.ca/~phil/courses/atsc301/downloads")
    return parser

def main(args=None):
    parser = make_parser()
    args=parser.parse_args(args)
    download(args.filename, root=args.root)

if __name__ == "__main__":
    main()
