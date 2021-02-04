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
import multiprocessing as mp
import random

#Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

PRIME_PROCESS_COUNT = 1
END_OF_NUMBERS = 'END'

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

# TODO create read_thread function
def read_file(queue, sem):
    with open('data.txt') as file1:
        for line in file1:
            queue.put(int(line))

    for i in range(PRIME_PROCESS_COUNT):
        queue.put(END_OF_NUMBERS)

# TODO create prime_process function
def process_prime(queue, p_list):
    while True:
        val = queue.get()
        if val == END_OF_NUMBERS:
            break
        
        if(is_prime(val)):
            p_list.append(val)


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

    # TODO Create shared data structres
    file_semaphore = threading.Semaphore(0)
    initial_queue = mp.Queue()
    primes = mp.Manager().list()

    # TODO create reading thread
    reader = threading.Thread(target=read_file, args=(initial_queue, file_semaphore))
    # TODO create prime processes
    prime_processes = [mp.Process(target=process_prime, args=(initial_queue, primes)) for i in range(PRIME_PROCESS_COUNT)]

    
    # TODO Start them all
    reader.start()
    for p in prime_processes:
        p.start()
    
    # TODO wait for them to complete
    reader.join()
    for p in prime_processes:
        p.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

