"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Brother Comeau

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread pools are not allowed
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE


4 is my score. I completed the assignment and got the recommended results. 
"""

import time
import queue
import threading
import random

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self):
        # TODO, you need to add arguments that will pass all of data that 1 factory needs
        # to create cars and to place them in a queue.
        self.car = Car()
        self.car_count = CARS_TO_PRODUCE
        self.cars_produced = 0

    def run(self, car_queue, sem):
        while self.cars_produced < self.car_count:
            # TODO Create a Car object and place it on a queue for the dealerships
            if car_queue.qsize() < MAX_QUEUE_SIZE:
                car_queue.put(self.car)
                self.cars_produced += 1

            sem.acquire()
                # Sleep a little - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 4))

class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self):
        # TODO, you need to add arguments that pass all of data that 1 factory needs
        # to create cars and to place them in a queue
        self.cars_sold = 0
        self.cars_to_sell = CARS_TO_PRODUCE

    def run(self, car_queue, sem, queue_stats):
        while True:
            # TODO process a car if there is one
            if car_queue.qsize() > 0:
                if car_queue.qsize() > 0:
                    queue_stats[car_queue.qsize() - 1] += 1
                car_queue.get()
                self.cars_sold += 1
            if self.cars_sold == self.cars_to_sell:
                return

            sem.release()
            # Sleep a little - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))



def main():
    log = Log(show_terminal=True)

    # TODO Create semaphore(s) ?
    # TODO Create queue(s) ?
    # TODO Create lock(s) ?
    sem = threading.Semaphore(MAX_QUEUE_SIZE)
    car_queue = queue.Queue(MAX_QUEUE_SIZE)
    
    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # TODO create your one factory
    factory = Factory()
    
    # TODO create your one dealership
    dealer = Dealer()
    # changed from Dealer.run() 

    log.start_timer()

    # TODO Start factory and dealership
    threads = []
    threads.append(threading.Thread(target=factory.run, args=(car_queue, sem)))
    threads.append(threading.Thread(target=dealer.run, args=(car_queue, sem, queue_stats)))

    for thread in threads:  # Starts all the threads.
        thread.start()
    for thread in threads:  # Waits for threads to complete before moving on with the main script.
        thread.join()
    # TODO Wait for factory and dealership to complete

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()

