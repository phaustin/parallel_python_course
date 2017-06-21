#include <time.h>
#include <sys/time.h>
#include <math.h>
#include <iostream>
#include <omp.h>
#include <stdio.h>

using namespace std;

double get_wall_time(){
    struct timeval time;
    if (gettimeofday(&time,NULL)){
        //  Handle error
        return 0;
    }
    return (double)time.tv_sec + (double)time.tv_usec * .000001;
}
double get_cpu_time(){
    return (double)clock() / CLOCKS_PER_SEC;
}

int omp_get_thread_num();
int omp_num_threads();

int main(){

    //  Start Timers
    double wall0 = get_wall_time();
    double cpu0  = get_cpu_time();

    //  Perform some computation.
    double sum = 0;
    
#pragma omp parallel
{
  auto threadnum = omp_get_thread_num();
  //auto threadnum = omp_get_num_threads();
  //cout << "Thread rank: " << threadnum << endl;
  printf("Thread num %d\n",threadnum);
}
 
#pragma omp parallel for reduction(+ : sum)
    for (long long i = 1; i < 10000000000; i++){
        sum += log((double)i);
    }

    //  Stop timers
    double wall1 = get_wall_time();
    double cpu1  = get_cpu_time();

    cout << "Wall Time = " << wall1 - wall0 << endl;
    cout << "CPU Time  = " << cpu1  - cpu0  << endl;

    //  Prevent Code Elimination
    cout << endl;
    cout << "Sum = " << sum << endl;

}
