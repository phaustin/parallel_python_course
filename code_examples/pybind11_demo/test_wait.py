import thread_tools
print(thread_tools.__file__)
import time
print(dir(thread_tools))
import contexttimer
from thread_tools import wait_loop_nogil

nloops=500
with contexttimer.Timer(time.perf_counter) as pure_wall:
    with contexttimer.Timer(time.process_time) as pure_cpu:
        result=wait_loop_nogil(nloops)
print(f'pure python wall time {pure_wall.elapsed} and cpu time {pure_cpu.elapsed}')



