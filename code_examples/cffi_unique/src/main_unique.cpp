//int make_unique(double *in_vec,double *out_vec,int n);
#include <iostream>
#include <vector>
#include <cstdint>
#include "make_unique.h"

int main()
{
  std::vector<double> in_vec = {0, 5, 5, 1, 2,2,2, 3, 4,4,4,4,4, 5};
  int last = make_unique_double(in_vec.data(),in_vec.size());
  in_vec.resize(last);
  for (double n : in_vec){
    std::cout << n << ' ';
  }
   std::cout << '\n';
}
