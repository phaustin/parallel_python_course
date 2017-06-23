#!/bin/bash
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
module purge
module load gcc/5.2.0-experimental
export CXX=/global/software/gcc-5.2.0-rpath/bin/g++
export CC=/global/software/gcc-5.2.0-rpath/bin/gcc
python setup.py install --single-version-externally-managed --record=record.txt
#pip install --no-deps .
