#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdint>

template <typename T>
  uint64_t make_unique_T(T* in_vec, int n){
    std::sort(in_vec,in_vec + n);
    auto last = std::unique(in_vec,in_vec + n);
    int last_index = std::distance(in_vec,last);
    return last_index;
  }


extern "C" {
  uint64_t make_unique_double(double *in_vec, uint64_t n){
    return make_unique_T(in_vec,n);
  }
  uint64_t make_unique_float(float *in_vec, uint64_t n){
    return make_unique_T(in_vec,n);
  }
  int64_t make_unique_int64(int64_t *in_vec, uint64_t n){
    return make_unique_T(in_vec,n);
  }
  int32_t make_unique_int32(int32_t *in_vec, uint64_t n){
    return make_unique_T(in_vec,n);
  }
}  
  
    
