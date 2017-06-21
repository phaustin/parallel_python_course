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

PYBIND11_PLUGIN(thread_tools) {
    xt::import_numpy();
    py::module m("thread_tools", R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: thread_tools

        .. autosummary::
           :toctree: _generate

           thread_sleep
           get_thread_id
    )pbdoc");

    m.def("thread_sleep_nogil", &thread_sleep_nogil,R"pbdoc(
      thread_sleep(nsecs)

      Sleep a thread for a specified time in seconds without the gil
       
      Parameters
      ----------

      nsecs: float
        fractional number of seconds to sleep

      Returns
      -------

      None
      )pbdoc");

    m.def("thread_sleep_gil", &thread_sleep_gil, R"pbdoc(
      thread_sleep(nsecs)

      Sleep a thread for a specified time in seconds holding the gil
       
      Parameters
      ----------

      nsecs: float
        fractional number of seconds to sleep

      Returns
      -------

      None
      )pbdoc");

    
    m.def("get_thread_id", &get_thread_id);

    m.def("get_process_id", &get_process_id);

#ifdef VERSION_INFO
    m.attr("__version__") = py::str(VERSION_INFO);
#else
    m.attr("__version__") = py::str("dev");
#endif

    return m.ptr();
}
