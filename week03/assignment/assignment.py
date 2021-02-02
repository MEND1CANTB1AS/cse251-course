"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: Brother Comeau
Purpose: Video Frame Processing
Instructions:
- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

Comments
  My program converts the inputes to the create_new_frame function into a tuple
  in order to pass them into the function and target it it with processing pool.
  My score should be a 5.
------------------------------------------------------------------------------
"""

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
import os, sys
sys.path.append('../../code')
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4  

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 300

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(frame_list):
    img_file = frame_list[0]
    grn_file = frame_list[1]
    proc_file = frame_list[2]
    # this print() statement is there to help see which frame is being processed
    #print(f'{proc_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(img_file)
    green_img = Image.open(grn_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(proc_file)


# TODO add any functions to need here
# # # # # def create_tuple(image_file, green_file, process_file):    
# # # # #     img_file = rf'elephant/image{image_number:03d}.png'
# # # # #     grn_file = rf'green/image{image_number:03d}.png'
# # # # #     proc_file = rf'processed/image{image_number:03d}.png'
# # # # #     return(img_file, grn_file, proc_file)



if __name__ == '__main__':
    # single_file_processing(300)
    # print('cpu_count() =', cpu_count())

    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpu_count = []
    yaxis_times = []

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpu_count and yaxis_times

    # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10
    frame_list = []  
    for image_number in range(1, FRAME_COUNT + 1):
        image_file = rf'elephant/image{image_number:03d}.png'
        green_file = rf'green/image{image_number:03d}.png'
        process_file = rf'processed/image{image_number:03d}.png'
        frame_list.append((image_file, green_file, process_file)) 
        
    #print(frame_list)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
    start_time = timeit.default_timer()
    time_list = [0]
    for CPU in range(1, CPU_COUNT + 1):    
        with mp.Pool(CPU) as p:
            p.map(create_new_frame, frame_list)
            time_list.append(timeit.default_timer() - all_process_time)
            
            # create_new_frame(frame_list)
            print(f'\nTime To Process all images = {time_list[-1] - time_list[-2]}') 
            log.write(f'Total Time for ALL procesing: {time_list[-1] - time_list[-2]}')
            yaxis_times.append(time_list[-1] - time_list[-2])
            xaxis_cpu_count.append(CPU)
    

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpu_count, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()