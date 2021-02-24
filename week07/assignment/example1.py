# Cube example using a pool map

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
    log = Log(filename_log='map.log', show_terminal=True)
    log.start_timer()
    pool = mp.Pool(4)
    results = pool.map(sum_all_values, range(100000000, 100000000 + 100))
    log.stop_timer('Finished: ')
    print(results)