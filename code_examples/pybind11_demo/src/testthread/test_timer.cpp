#include <time.h>
#include <sys/time.h>
#include <math.h>
#include <iostream>
#include <omp.h>
#include <stdio.h>
#include <chrono>
#include <thread>
#include <sstream>
#include <mutex>

using namespace std;

/** Thread safe cout class
  * Exemple of use:
  *    PrintThread{} << "Hello world!" << std::endl;
  */
//http://stackoverflow.com/questions/18277304/using-stdcout-in-multiple-threadsa

auto get_wall_time(){
  auto wcts = std::chrono::system_clock::now();
  return wcts;
}

auto get_cpu_time(){
  std::clock_t markcputime = std::clock();
  return markcputime;
}

void make_counter(int milsecs){
  std::this_thread::sleep_for(std::chrono::milliseconds(milsecs));
}

int main(){

    //  Start Timers
    auto wall0 = get_wall_time();
    auto cpu0  = get_cpu_time();

    //  Perform some computation.
    double sum = 0;

  #pragma omp parallel num_threads(4)
  {    
  auto threadnum = omp_get_thread_num();
  auto hasher=std::hash<std::thread::id>();
  auto this_id = hasher(std::this_thread::get_id());
  if(threadnum==0){
    auto threadtot  = omp_get_num_threads();
    cout << "Thread tot: " << threadtot << endl << flush;
  }
  make_counter(1000);
  printf("Thread num %d, c++ string id %x\n",threadnum,(uint64_t)this_id);
  string thread_id = to_string((uint64_t)this_id);
  printf("using to_string for thread_id: %s\n",thread_id.c_str());
  char buffer [9];
  int cx = snprintf ( buffer, 9, "%x",(uint64_t)this_id);
  printf("using snprintf for thread_id: %s\n",string(buffer).c_str());
    }
    //  Stop timers
    auto wall1 = get_wall_time();
    auto cpu1  = get_cpu_time();

    std::chrono::duration<double> wctduration = (wall1 - wall0);
    cout << "Wall Time = " << wctduration.count() << endl;
    cout << "CPU Time  = " << (cpu1  - cpu0)/(double) CLOCKS_PER_SEC  << endl;
    cout << "begin CPU Time  = " << (double) cpu0 << endl;
    cout << "end CPU Time  = " << (double) cpu1 << endl;
    cout << "clocks per second: " << (double) CLOCKS_PER_SEC << endl;
    cout << "begi wall time: " << std::chrono::system_clock::to_time_t(wall0) << endl;
    cout << "end wall time: " << std::chrono::system_clock::to_time_t(wall1) << endl;
    //  Prevent Code Elimination
    cout << endl;
    cout << "Sum = " << sum << endl;
}
