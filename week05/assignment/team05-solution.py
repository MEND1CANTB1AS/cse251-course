"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread/process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import queue
import multiprocessing as mp
import random

#Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

PRIME_PROCESS_COUNT = 1
NO_MORE = 'the end'

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

#  create read_thread function
def reader_func(filename, q, values_in_queue):
    with open(filename) as f:
        for line in f:
            line = line.strip()
            q.put(line)
            values_in_queue.release()

    for _ in range(PRIME_PROCESS_COUNT):
        q.put(NO_MORE)
        values_in_queue.release()

# create prime_process function
def process_prime(q, primes, values_in_queue):
    while True:
        values_in_queue.acquire()  # blocking
        value = q.get(block=False)
        print(value)
        if value == NO_MORE:
            return
        if (is_prime(int(value))):
            primes.append(int(value))



def create_data_txt(filename):
    with open(filename, 'w') as f:
        for _ in range(1000):
            f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # Create shared data structres
    # q.get(block=False)
    reader_queue = mp.Queue()

    primes = mp.Manager().list()

    values_in_queue = mp.Semaphore(0)

    #  create reading thread
    reader = threading.Thread(target=reader_func, args=(filename, reader_queue, values_in_queue))

    #  create prime processes
    processes = []
    for i in range(PRIME_PROCESS_COUNT):
        proc = mp.Process(target=process_prime, args=(reader_queue, primes, values_in_queue))
        processes.append(proc)

    #  Start them all
    for p in processes:
        p.start()
    reader.start()

    # wait for them to complete
    reader.join()
    for p in processes:
        p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

