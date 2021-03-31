"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: <Add name here>

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the end position.

What would be your strategy?  

Add backtracking on the threads that hit a dead end and pop them off of the path.
This will return the final path to the exit. You can then color in the path that is returned


Why would it work?

Threads do not run in parallel so when a thread hits the end it can pop the path values
before another thread will start.

"""
import math
import threading 
from screen import Screen
from maze import Maze

import cv2

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color


def solve_find_end(maze, path=None, threads=None, color=None):
    """ finds the end position using threads.  Nothing is returned """
    # When one of the threads finds the end position, stop all of them
    global thread_count
    global stop
    if threads is None:
        threads = []
    if path is None:
        path = []
    if color is None:
        color = get_color()
    if len(path) == 0:
        pos = maze.get_start_pos()
        path.append(pos)
        maze.move(path[0][0], path[0][1], color)
        stop = False
    else:
        pos = path[-1]
        maze.move(path[-1][0], path[-1][1], color)
    if stop:
        return
    if maze.at_end(path[-1][0], path[-1][1]):
        stop = True
        return
    else:
        pos_moves = maze.get_possible_moves(path[-1][0], path[-1][1])
        if len(pos_moves) >= 1:
            path.append(pos_moves[0])
            if len(path) == 2:
                threads.append(threading.Thread(target=solve_find_end, args=(maze, path, threads, color)))
                thread_count += 1
                threads[0].start()
                threads[0].join()
            else:
                solve_find_end(maze, path, threads, color)
        if len(pos_moves) >= 2:
            for move in range(1, len(pos_moves)):
                path.append(pos_moves[move])
                threads.append(threading.Thread(target=solve_find_end, args=(maze, path, threads)))
                thread_count += 1
                num = len(threads) - 1
                threads[num].start()
                threads[num].join()
            
        return


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()