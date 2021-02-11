"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

After you can copy a text file word by word exactly
- Change the program to be faster (Still using the processes)

"""

import multiprocessing as mp
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

def sender(conn, count, filename1):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''

    with open(filename1, 'r') as f:
        for line in f:
            conn.send(line)
            count.value += 1

    conn.send(None)

def receiver(conn, filename):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename, 'w') as f:
        while True:
            data = conn.recv()
            if (data is None):
                break

            f.write(data)


def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    parent_pipe, child_pipe = mp.Pipe()
    
    # TODO create variable to count items sent over the pipe
    num = Value('i', 0)

    # TODO create processes 
    processes = []
    processes.append(mp.Process(target=sender, args=(parent_pipe, num, filename1)))
    processes.append(mp.Process(target=receiver, args=(child_pipe, filename2)))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    for p in processes:
        p.start()

    # TODO wait for processes to finish
    for p in processes:
        p.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {num.value}: ')
    log.write(f'items / second = {num.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    # copy_file(log, 'bom.txt', 'bom-copy.txt')

