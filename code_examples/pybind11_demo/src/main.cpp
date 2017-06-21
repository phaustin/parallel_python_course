#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdio.h>
#include <chrono>
#include <thread>
#include <typeinfo>
#include "xtensor/xmath.hpp"              // xtensor import for the C++ universal functions
#define FORCE_IMPORT_ARRAY                // numpy C api loading
#include "xtensor-python/pyarray.hpp"     // Numpy bindings
#include "xtensor-python/pytensor.hpp"
#include "xtensor/xtensor.hpp"
#include "xtensor/xview.hpp"
#include "cffi_headers/c_lib.h"


using namespace std;

auto get_wall_time(){
  auto wcts = std::chrono::system_clock::now();
  return wcts;
}


namespace py = pybind11;

//c++ version of our numba wait_loop

auto wait_loop(int n){
  double out;
  auto nvec =  xt::arange(0, n);
  for (auto m : nvec){
    auto mvec = xt::arange(0, m);
    for(auto l: mvec){
      auto jvec = xt::arange(0, l);
         for(auto j: jvec){
           auto ivec = xt::arange(0, j);
           for(auto i: ivec){
             i=i+4;
             out =std::sqrt(i);
             out=std::pow(out,2.);
         }
      }
    }
  }
  return out;
}
    
PYBIND11_PLUGIN(thread_tools) {
    xt::import_numpy();
    py::module m("thread_tools", R"pbdoc(
        Pybind11 example plugin
        -----------------------

    )pbdoc");

    m.def("thread_sleep_nogil", &thread_sleep_nogil,R"pbdoc(
      thread_sleep(nsecs)

      Sleep a thread for a specified time in seconds without the gil

      )pbdoc");

    m.def("thread_sleep_gil", &thread_sleep_gil, R"pbdoc(
      thread_sleep(nsecs)

      Sleep a thread for a specified time in seconds holding the gil

      )pbdoc");

    m.def("get_thread_id", &get_thread_id, py::call_guard<py::gil_scoped_release>(),
          "get thread id with C++ call");

    m.def("get_process_id", &get_process_id,py::call_guard<py::gil_scoped_release>(),
          "get process id with C++ call");

    m.def("wait_loop_nogil", &wait_loop,py::call_guard<py::gil_scoped_release>(),
          "wait loop without the gil");
    
#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}
