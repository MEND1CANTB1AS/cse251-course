"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- NO global variables!!!
- Don't use thread/process pools for this program.
- Use only the provided packages that are imported.
- I would suggest setting RETRIEVE_THREADS to 1 and get that to work.
  Then increase it.

"""

import threading
import queue
import requests

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q, sem, log):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        sem.acquire()
        # TODO process the value retrieved from the queue
        
        url = q.get()
        response = requests.get(url)
        if url == NO_MORE_VALUES:
            print("done")
            return
        elif response.status_code == 200:
            data = response.json()
            print(f'Name = {data["name"]}')
        else:
            print('Response = ', response.status_code)
        # TODO make Internet call to get characters name and log it



def file_reader(q, sem, log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """
    
    # TODO Open the data file "data.txt" and place items into a queue
    with open('data.txt') as file:
        for line in file:
            line = line.strip()
            q.put(line)
            sem.release()
    q.put(NO_MORE_VALUES)
    sem.release()
    log.write('finished reading file')
    q.put(NO_MORE_VALUES)
    sem.release()
    # TODO signal the retrieve threads one more time that there are "no more values"
##### response = requests.get(self.url)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue and semaphore
    url_queue = queue.Queue()
    sem = threading.Semaphore(0)

    reader = threading.Thread(target=file_reader, args=(url_queue, sem, log))
    getters = [threading.Thread(target=retrieve_thread, args=(url_queue, sem, log)) for _ in range(4)]
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job

    log.start_timer()

    # TODO Get them going - The order doesn't matter
    for p in getters:
        p.start()
    reader.start()
    # TODO Wait for them to finish - The order doesn't matter
    for p in getters:
        p.join()
    reader.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




