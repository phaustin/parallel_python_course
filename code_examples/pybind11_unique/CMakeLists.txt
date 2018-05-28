cmake_minimum_required(VERSION 3.8)
project(cpp_make_unique)

if (NOT (DEFINED "ENV{PREFIX}"))
     set(PREFIX $ENV{CONDA_PREFIX})
else()
     set(PREFIX $ENV{PREFIX})
endif()

set(CMAKE_MODULE_PATH "${PREFIX}/lib/cmake/xtensor"
"${PREFIX}/lib/cmake/xtensor-python"  "${PREFIX}/share/cmake/pybind11"  "${CMAKE_MODULE_PATH}")
include(pybind11Tools)
include(xtensorConfig)
SET(CMAKE_C_COMPILER $ENV{CC})
SET(CMAKE_CXX_COMPILER $ENV{CXX})
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_VERBOSE_MAKEFILE ON)
pybind11_add_module(cpp_make_unique src/main.cpp)
include_directories(${xtensor_INCLUDE_DIRS} ${NUMPY_INCLUDE})
