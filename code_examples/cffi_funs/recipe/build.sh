#!/bin/bash
export GXX=/home/phil/ana36/bin/x86_64-conda_cos6-linux-gnu-g++
export CXX=$GXX
cmake -DCMAKE_CXX_COMPILER=$GXX -DCMAKE_INSTALL_PREFIX=$PREFIX $SRC_DIR
make install
