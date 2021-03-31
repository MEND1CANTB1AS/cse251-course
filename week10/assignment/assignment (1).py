"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: <your name>

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will "write"/send numbers to the reader.  
  To keep things simple, send random values from 0 to 255 to the reader.

- reader: a process that receive numbers sent by the writer.

- You don't need any sleep() statements for either process.

- You are able to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".

- You must use ShareableList between the two processes.  
  You are only allowed to use BUFFER_SIZE number of positions
  in this ShareableList for tranfering data from the writer to
  the reader.  However, you can use other parts of the ShareableList
  for other purposes if you want by increasing the size of the ShareableList.
  This buffer area will act like a queue - First In First Out.

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

Add any comments for me:



"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10

def write(shared_list, items_sent, items_to_send, sem, lock):
  print("write")
  while items_sent < items_to_send:
    for i in range(0, BUFFER_SIZE):
      lock.acquire()
      if shared_list[i] == -1:
        shared_list[i] = random.randint(0, 255)
        lock.release()
        items_sent += 1
        #sem.acquire()
        break
    # sem.acquire()
      else:
        lock.release()
    sem.acquire()
  return

def read(shared_list, items_read, items_to_read, sem, lock):
  print("Read")
  while items_read < items_to_read:
    for i in range(0, BUFFER_SIZE):
      lock.acquire()
      if shared_list[i] > -1:
        #print("Popping: ", i, ": ", shared_list[i])
        shared_list[i] = -1
        lock.release()
        items_read += 1
        break
      else:
        lock.release()
    sem.release()
  shared_list[-1] = items_read
  return

def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(100000, 1000000)
    smm = SharedMemoryManager()
    smm.start()

    # Create a ShareableList to be used between the processes
    size = BUFFER_SIZE + 2
    shared_list = smm.ShareableList(range(size))
    for i in range(0, size):
      shared_list[i] = -1

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    lock = mp.Lock()
    sem = mp.Semaphore(BUFFER_SIZE)

    # TODO - create reader and writer processes
    items_sent = 0
    items_read = 0
    p1 = mp.Process(target=write, args=(shared_list, items_sent, items_to_send, sem, lock))
    p2 = mp.Process(target=read, args=(shared_list, items_read, items_to_send, sem, lock))

    # TODO - Start the processes and wait for them to finish
    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print(f'{items_to_send} sent by the writer')

    # TODO - Display the number of numbers/items received by the reader.
    print(f'{shared_list[-1]} read by the reader')

    smm.shutdown()


if __name__ == '__main__':
    main()
