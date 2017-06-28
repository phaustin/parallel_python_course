project(thread_tools)
cmake_minimum_required(VERSION 3.8)
if (APPLE)
   SET(CMAKE_C_COMPILER clang)
   SET(CMAKE_CXX_COMPILER clang++)
endif(APPLE)
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_VERBOSE_MAKEFILE ON)
set(CMAKE_MODULE_PATH "${CONDA_CMAKE};${CMAKE_MODULE_PATH}")
message("pha here is CMAKE_MODULE_PATH: ${CMAKE_MODULE_PATH}")
include(pybind11Tools)
include(xtensorConfig)
message("here is xtensor_INCLUDE_DIRS: ${xtensor_INCLUDE_DIRS}")
pybind11_add_module(${CMAKE_MODULE_NAME} src/main.cpp)
include_directories(${xtensor_INCLUDE_DIRS} ${NUMPY_INCLUDE})
target_link_libraries(${CMAKE_MODULE_NAME} PUBLIC ${CFFI_LIB})



