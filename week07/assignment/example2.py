# Cube example using pool apply_asyc()

import multiprocessing as mp 

import os, sys
sys.path.append('../../code')
from cse251 import *

def sum_all_values(x):
    total = 0
    for i in range(1, x + 1):
        total += i
    return total
    
if __name__ == "__main__":
    log = Log(filename_log='apply_async.log', show_terminal=True)
    log.start_timer()
    pool = mp.Pool(4)
    results = [pool.apply_async(sum_all_values, args=(x,)) for x in range(10000, 10000 + 10)]

	# do something else

    output = [p.get() for p in results]
    log.stop_timer('Finished: ')
    print(output)