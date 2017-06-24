project(unique_lib)
cmake_minimum_required(VERSION 3.8)
project(make_unique)
if (APPLE)
  set(CMAKE_CXX_COMPILER clang++)
  set(CMAKE_C_COMPILER clang)
endif(APPLE)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_VERBOSE_MAKEFILE ON)
SET(CMAKE_SKIP_BUILD_RPATH  FALSE)
SET(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE) 
SET(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
FILE(GLOB files_cpp src/make_unique.cpp)
add_library(make_unique SHARED ${files_cpp})
set(LIBRARY_OUTPUT_DIRECTORY ${CMAKE_INSTALL_PREFIX}/lib)
set_target_properties(make_unique PROPERTIES SUFFIX .so)

install(TARGETS make_unique
        LIBRARY DESTINATION "${CMAKE_INSTALL_PREFIX}/lib")

# add_custom_command(TARGET make_unique POST_BUILD
#                    COMMAND ${CMAKE_COMMAND} -E copy_directory
#                        ${CMAKE_SOURCE_DIR}/make_unique_headers ${CMAKE_INSTALL_PREFIX}/include)

install(DIRECTORY ${CMAKE_SOURCE_DIR}/make_unique_headers
        DESTINATION include)

