#!/bin/bash
unset MACOSX_DEPLOYMENT_TARGET
export GXX=/home/phil/ana36/bin/x86_64-conda_cos6-linux-gnu-g++
export CXX=$GXX
python setup.py install --single-version-externally-managed --record=record.txt
