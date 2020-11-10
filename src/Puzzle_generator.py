# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 21:39:13 2020

@author: # By Ihsaan Malek and Olivier Racette
    
Generate Random puzzles for 2.4 and 2.5
"""
import numpy as np
import os
from pathlib import Path

puzzle_folder = Path("../puzzles/")

def generate_random_puzzles(num_puzzles,num_row,num_col):
    
    file_name ='{}_puzzles_{}X{}.txt'.format(num_puzzles,num_row,num_col)
    
    if os.path.exists(puzzle_folder/file_name): 
        os.remove(puzzle_folder/file_name)      #optional can be removed from code
        print('removing old puzzle list')
    
    print('Creating {} Random Puzzles, size: {} rows by {} columns'.format(num_puzzles,num_row,num_col))
    
    puzzle_file = open(puzzle_folder/file_name, 'w')
    puzzle_length= num_row*num_col
    
    for row in range(num_puzzles):
        np.savetxt(puzzle_file,[np.random.permutation(puzzle_length).astype(int)], fmt='%i', delimiter=',')
    
    puzzle_file.close()
    
    return 0

#generate_random_puzzles(3,2,4)