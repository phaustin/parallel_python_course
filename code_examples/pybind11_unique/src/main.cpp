#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>

#include "pybind11/pybind11.h"

#include "xtensor/xmath.hpp"
#include "xtensor/xarray.hpp"

#define FORCE_IMPORT_ARRAY
#include "xtensor-python/pyarray.hpp"
#include "xtensor-python/pyvectorize.hpp"
#include "xtensor-python/pytensor.hpp"

template <typename T>
  uint64_t make_unique_T(T* in_vec, int n){
    std::sort(in_vec,in_vec + n);
    auto last = std::unique(in_vec,in_vec + n);
    int last_index = std::distance(in_vec,last);
    return last_index;
  }


extern "C" {
  uint64_t make_unique_double(xt::pytensor<double,1>& py_vec, uint64_t n){
    double* in_vec = py_vec.raw_data();
    return make_unique_T(in_vec,n);
  }
  uint64_t make_unique_float(xt::pytensor<float,1>& py_vec, uint64_t n){
    float* in_vec = py_vec.raw_data();
    return make_unique_T(in_vec,n);
  }
  int64_t make_unique_int64(xt::pytensor<int64_t,1>& py_vec, uint64_t n){
    int64_t *in_vec = py_vec.raw_data();
    return make_unique_T(in_vec,n);
  }
  int64_t make_unique_int32(xt::pytensor<int32_t,1>& py_vec, uint64_t n){
    int32_t *in_vec = py_vec.raw_data();
    return make_unique_T(in_vec,n);
  }
}  


namespace py = pybind11;

PYBIND11_PLUGIN(cpp_make_unique) {
  xt::import_numpy();

  py::module m("cpp_make_unique", R"pbdoc(
        Pybind11 example plugin

    )pbdoc");

    m.def("make_unique_double", &make_unique_double, R"pbdoc(
       docstring   
    )pbdoc");

    m.def("make_unique_float", &make_unique_float, R"pbdoc(
       docstring   
    )pbdoc");

    m.def("make_unique_int64", &make_unique_int64, R"pbdoc(
        docstring  
    )pbdoc");
    
    m.def("make_unique_int32", &make_unique_int32, R"pbdoc(
        docstring  
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}
