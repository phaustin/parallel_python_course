import thread_tools
import time
print('imported from thread_tools: ',dir(thread_tools))
import contexttimer
from thread_tools import wait_loop_nogil

nloops=500
with contexttimer.Timer(time.perf_counter) as pure_wall:
    with contexttimer.Timer(time.process_time) as pure_cpu:
        result=wait_loop_nogil(nloops)
print(f'pybind11 wall time {pure_wall.elapsed} and cpu time {pure_cpu.elapsed}')



