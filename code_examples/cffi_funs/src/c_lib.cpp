#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <stdio.h>
#include <chrono>
#include <thread>
#include <sys/types.h>
#include <stdint.h>

//https://stackoverflow.com/questions/17432502/how-can-i-measure-cpu-time-and-wall-clock-time-on-both-linux-windows
using namespace std;

auto get_wall_time(){
  auto wcts = std::chrono::system_clock::now();
  return wcts;
}

extern "C" {

#ifdef _WIN32
#include  <process.h>
void get_process_id(char* buffer){
  int this_id = _getpid();
  int cx = snprintf ( buffer, 9, "%d",this_id);
}  
#else
#include <unistd.h>
void get_process_id(char* buffer){
  pid_t this_id = getpid();
  int cx = snprintf ( buffer, 9, "%jd",(intmax_t) this_id);
}  
#endif
  
double get_cpu_time(){
  std::clock_t markcputime = std::clock();
  return (double)markcputime;
}

void thread_sleep_gil(float secs){
  int milsecs=(int)(secs*1000);
  std::this_thread::sleep_for(std::chrono::milliseconds(milsecs));
}

void thread_sleep_nogil(float secs){
  int milsecs=(int)(secs*1000);
  std::this_thread::sleep_for(std::chrono::milliseconds(milsecs));
}

void get_thread_id(char* buffer){
  auto hasher=std::hash<std::thread::id>();
  uint64_t this_id = (uint64_t)hasher(std::this_thread::get_id());
  int cx = snprintf ( buffer, 9, "%llx",this_id);
}
}
