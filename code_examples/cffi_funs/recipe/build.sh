#!/bin/bash
cmake -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_INSTALL_PREFIX=$PREFIX $SRC_DIR
make install
