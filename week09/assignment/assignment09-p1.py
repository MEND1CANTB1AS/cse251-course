"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: <Add name here>

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze

import cv2

# Include cse 251 common Python files - Dont change
import os, sys
sys.path.append('../../code')
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions
# path[-1][0], path[-1][1]

def solve_path(maze, path=None):
    """ Solve the maze and return the path.  The path is a list of positions, (x, y) """
    # TODO start add code here
    if path is None:
        path = []
    if len(path) == 0:
        print("Length 0")
        pos = maze.get_start_pos()
        path.append(pos)
        maze.move(path[0][0], path[0][1], COLOR)
        # print("Path Empty")
    else:
        pos = path[-1]
        maze.move(path[-1][0], path[-1][1], COLOR)
        # print("Path Not Empty")
    
    
    if maze.at_end(path[-1][0], path[-1][1]):
        print("Final Position: ", path[-1])
        return path
    else:
        print(path[-1])
        pos_moves = maze.get_possible_moves(path[-1][0], path[-1][1])
        # print("Pos_Moves ", pos_moves)
        if len(pos_moves) > 0:
            path.append(pos_moves[0])
            solve_path(maze, path)
        else:
            print("Dead End")
            maze.restore(path[-1][0], path[-1][1])
            path.pop()
            solve_path(maze, path)
        return path    
    
    
    


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

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
    
    return path

# 'large.bmp',
def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp',  'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()
    