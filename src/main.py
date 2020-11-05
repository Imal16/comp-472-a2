# By Ihsaan Malek and Olivier Racette
# The goal of this program is to use several search algorithms (UCS, GBFS, A*) to complete an x-puzzle.

# Legal moves:
#   direct horizontal / vertical translation (cost 1)
#   wrapping horizontal / vertical translation (cost 2) NOTE: vertical wrapping is only OK when there are more than 2 rows
#   diagonal (direct or wrap) (cost 3)

import csv
import argparse
import numpy as np

from node import Node
from pathlib import Path

puzzle_folder = Path("../puzzles/")

#Leaving this here for now. Would be great if it wasn't hard coded but we don't really have a way of doing it another way with the data format.
#We can't really infer the dimensions of the puzzle from the txt file
#8 puzzle is supposed to be 3x3 grid, but our version has 8-puzzle being 2x4 grid...
puzzle_rows = 2
puzzle_cols = 4


#Placeholder for a method that takes in a node (any node) and generates its immediate children
#Maybe we could make a tree class, idk.
def buildChildren(node):
    pass


#reads the given pizzle file
#returns a list of puzzles
def readPuzzle(file, p_rows, p_cols):
    puzzles = []

    with open(puzzle_folder / file) as csvFile:
        reader = csv.reader(csvFile, delimiter=' ')
        
        for row in reader:
            p = []

            #Entries are read as characters by default...need to iterate over each and read as int
            for entry in row:
                p.append(int(entry))

            #easy way of doing it, with numpy
            puzzles.append(np.array(p).reshape(p_rows, p_cols))     #add tolist() if python array/list is needed

    return puzzles


#Sets and retrieves the command line arguments
#Current arguments:
    #puzzle file to be used (optional, samplePuzzles.txt is used by default)
#Returns a Namespace object
def getArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file" ,type=str, help="Name of the puzzle file. Defaults to samplePuzzles.txt", default="samplePuzzles.txt")

    return parser.parse_args()



def run():
    args = getArgs()

    puzzles = readPuzzle(args.file, puzzle_rows, puzzle_cols)

    print(puzzles)
    
    root = Node(None, 0, 0, puzzles[0])

    #Each algorithm needs to be run on each puzzle
    #for p in puzzles:
        #root = Node(None, 0, 0, p)
 
        #run UCS

        #run GBFS heuristic 0 --> demo only?
        #run GBFS heuristic 1
        #run GBFS heuristic 2

        #run A* heuristic 0 --> demo only?
        #run A* heuristic 1
        #run A* heuristic 2

        #output the following files:
            #UCS solution, search
            #GBFS h1 solution, search
            #GBFS h2 solution, search
            #A* h1 solution, search
            #A* h2 solution, search

            #GBFS h0 solution, search --> demo only?
            #A* h0 solution, search --> demo only?

            #14 files total per puzzle

            #file name pattern: puzzleIndex_algorithm-heuristic_contents.txt
            

if __name__ == "__main__":
    run()