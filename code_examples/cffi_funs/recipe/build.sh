#!/bin/bash
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi
module load gcc/5.2.0-experimental
cmake -DCMAKE_CXX_COMPILER=/global/software/gcc-5.2.0-rpath/bin/g++ -DCMAKE_INSTALL_PREFIX=$PREFIX $SRC_DIR
make install
