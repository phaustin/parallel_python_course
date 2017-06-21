#!/bin/bash -v

export OMP_NUM_THREADS=12
# /usr/local/bin/g++  -fopenmp  -Dcmake_example_EXPORTS -I/Users/phil/mini36/include/python3.6m  -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk -fPIC   -std=c++14 -o wall_clock wall_clock.cpp

#/usr/local/bin/g++  -Dcmake_example_EXPORTS -I/Users/phil/mini36/include/python3.6m  -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk -fPIC   -std=c++14 -o testit threading.cpp

/usr/local/bin/g++  -fopenmp  -Dcmake_example_EXPORTS -I/Users/phil/mini36/include/python3.6m  -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.12.sdk -fPIC   -std=c++14 -o test_timer test_timer.cpp

./test_timer
rm test_timer
