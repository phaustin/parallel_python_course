#ifndef C_LIB_H
#define C_LIB_H

extern "C" {

#ifdef _WIN32
#include  <process.h>
#else
#include <unistd.h>
#endif
  
void get_process_id(char* buffer);
  
double get_cpu_time();
  
void thread_sleep_gil(float secs);
  
void thread_sleep_nogil(float secs);
  
void get_thread_id(char* buffer);

}  
#endif /* C_LIB_H */
