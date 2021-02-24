# Cube example using pool apply_asyc() and callback function

import multiprocessing as mp
import time

import os, sys
sys.path.append('../../code')
from cse251 import *

result_list = []

def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    return total

def log_result(result):
    # This is called whenever sum_all_values(i) returns a result.
    # result_list is modified only by the main process, not the pool workers.
    result_list.append(result)

def apply_async_with_callback():
    log = Log(filename_log='callback.log', show_terminal=True)
    log.start_timer()
    pool = mp.Pool(4)

    # Add job to the pool
    pool.apply_async(sum_all_values, args = (100000000, ), callback = log_result)
    
    time.sleep(1)       # Do something - this is the main thread sleeping

    pool.apply_async(sum_all_values, args = (100000001, ), callback = log_result)

    time.sleep(1)       # Do something

    pool.apply_async(sum_all_values, args = (100000002, ), callback = log_result)

    time.sleep(1)       # Do something

    pool.apply_async(sum_all_values, args = (100000003, ), callback = log_result)

	# Do something while the processes are doing their work

	# Need to know when the pool is finished
    pool.close()
    pool.join()

    log.stop_timer('Finished: ')

	# display the global variable of the results from the pool
    print(result_list)

if __name__ == '__main__':
    apply_async_with_callback()