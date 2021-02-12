"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Brother Comeau

Purpose: Processing Plant

Instructions:

- Implement the classes to allow gifts to be created.

"""

from datetime import datetime, timedelta
import random
import json
import threading
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import os.path
import datetime
import time

# Include cse 251 common Python files - Don't change
import os, sys
sys.path.append('../../code')
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'
DONE = "Done"

# No Global variables

class Bag():
    """ bag of marbles - Don't change for the 93% """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change for the 93% """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, settings):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marbles_produced = 0
        self.marble_count = settings[MARBLE_COUNT]
        self.wait = settings[CREATOR_DELAY]

    def run(self, parent_creator, settings):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        
        while self.marbles_produced < self.marble_count:
            self.marble = random.choice(self.colors)
            self.marbles_produced += 1
            #print(self.marble)
            parent_creator.send(self.marble)
            time.sleep(self.wait)
            #print("Sent a Marble")
        print("MP: ", self.marbles_produced)
        print("SENDING: DONE")
        parent_creator.send(DONE)
        

class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, settings):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.bag = Bag()
        self.bag_count = settings[BAG_COUNT]
        self.wait = settings[BAGGER_DELAY]

    def run(self, child_bagger, parent_bagger):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        while True:
            self.marble = child_bagger.recv()
            if self.marble != DONE:
                self.bag.add(self.marble)
                # print('Bagging: ', self.marble)
                if self.bag.get_size() == self.bag_count:
                    # print(self.bag)
                    parent_bagger.send(self.bag)
                    # print("Sent a Bag")
                    self.bag = Bag()
                    time.sleep(self.wait)
            else:    
                parent_bagger.send(DONE)
                print('No More Marbles to Bag')
                return


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, settings):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.wait = settings[ASSEMBLER_DELAY]

    def run(self, child_assembler, parent_assembler):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True: 
            self.bag = child_assembler.recv()
            if self.bag != DONE:
                self.big_marble = random.choice(self.marble_names)
                self.gift = Gift(self.big_marble, self.bag)
                # print(self.gift)
                parent_assembler.send(self.gift)
                # print("Sent a Gift to the Wrapper")
                time.sleep(self.wait)
            else:
                parent_assembler.send(DONE)
                print("Done Assembling")
                return
            

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, settings):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.wait = settings[WRAPPER_DELAY]

    def run(self, child_wrapper):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(BOXES_FILENAME, 'w') as f:
            while True:
                self.gift = child_wrapper.recv()
                if self.gift != DONE:
                    
                    self.data = self.gift.__str__()
                    # print(self.data)
                    self.time = str(datetime.now().time())
                    f.write("Created - " + self.time + ": " + self.data + "\n")
                    
                    # print("Wrote to File")
                    time.sleep(self.wait)
                else:
                    f.close()
                    print("Done Wrapping")
                    return
                    

def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """
    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator = Marble_Creator(settings)
    bagger = Bagger(settings)
    assembler = Assembler(settings)
    wrapper = Wrapper(settings)
    
    parent_creator, child_bagger = mp.Pipe()
    parent_bagger, child_assembler = mp.Pipe()
    parent_assembler, child_wrapper = mp.Pipe()

    # TODO create variable to be used to count the number of gifts

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    processes = []
    processes.append(mp.Process(target=creator.run, args=(parent_creator, settings)))
    processes.append(mp.Process(target=bagger.run, args=(child_bagger, parent_bagger)))
    processes.append(mp.Process(target=assembler.run, args=(child_assembler, parent_assembler)))
    processes.append(mp.Process(target=wrapper.run, args=(child_wrapper,)))
    


    log.write('Starting the processes')
    # TODO add code here
    for process in processes:
        process.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    for process in processes:
        process.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.



if __name__ == '__main__':
    main()

