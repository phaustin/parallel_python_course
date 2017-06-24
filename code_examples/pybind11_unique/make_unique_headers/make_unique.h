#ifndef MAKE_UNIQUE_H
#define MAKE_UNIQUE_H

#include <cstdint>

extern "C" {
  uint64_t make_unique_float64(double *in_vec, uint64_t n);

  uint64_t make_unique_float32(float *in_vec, uint64_t n);

  int64_t make_unique_int64(int64_t *in_vec, uint64_t n);

  int64_t make_unique_int32(int32_t *in_vec, uint64_t n);

}  

#endif /*C_LIB_H*/
