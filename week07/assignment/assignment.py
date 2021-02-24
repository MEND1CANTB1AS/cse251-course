"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>

Purpose: Process Task Files

Instructions:

- run the Python program "create_tasks.py" to create the task files.
- There are 5 different tasks that need to be processed.  Each task needs to
  have it's own process pool.  The number of processes in each pool is up to
  you.  However, your goal is to process all of the tasks as quicky as possible
  using these pools.  You will need to try out different pool sizes.
- The program will load a task one at a time and add it to the pool that is used
  to process that task type.  You can't load all of the tasks into memory/list and
  then pass them to a pool.
- You are required to use the function apply_async() for these 5 pools. You can't
  use map(), or any other pool function.
- Each pool will collect that results of their tasks into a global list.
  (ie. result_primes, result_words, result_upper, result_sums, result_names)
- the task_* functions contain general logic of what needs to happen


TODO

Add you comments here on the pool sizes that you used for your assignment and
why they were the best choices.

The smallest pool size was the uppercase as it required the least amount of resources.
My total pool size was set over my number of cores as that ended up increasing my performance 
by about 12 seconds. Some of the processes are shared between the pools allowing for faster 
completion than simply limiting the pool size totals to 8.

"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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

def task_prime(value):
    """
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        string = str(value) + " is prime"
    else:
        string = str(value) + " is not prime"
    return string

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    string = str(word)
    found = False
    with open('words.txt', 'r') as f:
        for line in f:
            if line == word:
                found = True
    f.close()
    if found:
        string += " Found"
    else:
        string += " not found"

    #result_words.append(string)
    return string

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    # result_upper.append(text.upper())
    string = str(text) + " ==> " + str(text.upper())
    return string

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total_sum = 0
    string = "sum of " + str(start_value) + " to " + str(end_value) + " = "
    for i in range(start_value, end_value):
        total_sum += i

    string += str(total_sum)
    # result_sums.append(string)
    return string

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)
    if response.status_code == 200:
        response = response.json()
    else:
        print('RESPONSE = ', response.status_code)
    string = url + " has name " + response['name']
    return string
    # result_names.append(response['name'])

def prime_callback(result):
    result_primes.append(result)

def sum_callback(result):
    result_sums.append(result)

def upper_callback(result):
    result_upper.append(result)

def word_callback(result):
    result_words.append(result)

def url_callback(result):
    result_names.append(result)

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool_prime = mp.Pool(2)
    pool_word = mp.Pool(2)
    pool_name = mp.Pool(4)
    pool_upper = mp.Pool(1)
    pool_sum = mp.Pool(3)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args=(task["value"], ), callback = prime_callback)
            # task_prime(task['value'])
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args=(task['word'], ), callback = word_callback)
            # task_word(task['word'])
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args=(task['text'], ), callback = upper_callback)
            # task_upper(task['text'])
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args=(task['start'], task['end'] ), callback = sum_callback)
            # task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args=(task['url'], ), callback = url_callback)
            # task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools
    pool_prime.close()
    pool_prime.join()

    pool_word.close()
    pool_word.join()

    pool_upper.close()
    pool_upper.join()

    pool_sum.close()
    pool_sum.join()

    pool_name.close()
    pool_name.join()





    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')

    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Primes: {len(result_primes)}')
    log.write(f'Words: {len(result_words)}')
    log.write(f'Uppercase: {len(result_upper)}')
    log.write(f'Sums: {len(result_sums)}')
    log.write(f'Names: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
