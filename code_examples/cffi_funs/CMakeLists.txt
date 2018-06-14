project(cffi_funs)
#set(CMAKE_CXX_COMPILER $CXX)
cmake_minimum_required(VERSION 3.8)
#call with cmake  -DCMAKE_INSTALL_PREFIX=$PREFIX $SRC_DIR
message("here is install directory: ${CMAKE_INSTALL_PREFIX}")
set(CMAKE_C_COMPILER $CC)
set(CMAKE_CXX_STANDARD 14) # C++11...
set(CMAKE_CXX_STANDARD_REQUIRED ON) #...is required...
set(CMAKE_CXX_EXTENSIONS OFF) #...without compiler extensions like gnu++11
set(CMAKE_VERBOSE_MAKEFILE ON)
FILE(GLOB files_cpp "${CMAKE_SOURCE_DIR}/src/*.cpp")
SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
add_library(cffi_funs SHARED ${files_cpp})
set_target_properties(cffi_funs PROPERTIES SUFFIX .so)


install(TARGETS cffi_funs
        LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/lib")

install(DIRECTORY ${CMAKE_SOURCE_DIR}/cffi_headers
        DESTINATION include)

