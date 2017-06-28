#!/bin/bash
unset MACOSX_DEPLOYMENT_TARGET
python setup.py install --single-version-externally-managed --record=record.txt
