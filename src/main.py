# By Ihsaan Malek and Olivier Racette
# The goal of this program is to use several search algorithms (UCS, GBFS, A*) to complete an x-puzzle.

import csv
import argparse
import random

#External dependencies
import numpy as np

from node import Node
from node_util import buildChildren, printBoard
from Search_functions import generate_goal, manhattan_distance, sum_permutation_inversions, A_star
from pathlib import Path

puzzle_folder = Path("../puzzles/")

#Leaving this here for now. Would be great if it wasn't hard coded but we don't really have a way of doing it another way with the data format.
#We can't really infer the dimensions of the puzzle from the txt file
#8 puzzle is supposed to be 3x3 grid, but our version has 8-puzzle being 2x4 grid...
puzzle_rows = 2 # might need to change this so it can recognize it dynamically for 2.5
puzzle_cols = 4 # might need to change this so it can recognize it dynamically for 2.5

#reads the given pizzle file
#returns a list of puzzles
def readPuzzle(file, p_rows, p_cols):
    puzzles = []
    max_val = []

    with open(puzzle_folder / file) as csvFile:
        reader = csv.reader(csvFile, delimiter=' ')
        
        for row in reader:
            p = []

            #Entries are read as characters by default...need to iterate over each and read as int
            for entry in row:
                p.append(int(entry))
            max_val.append(max(p))
            #easy way of doing it, with numpy
            puzzles.append(np.array(p).reshape(p_rows, p_cols))     #add tolist() if python array/list is needed
    
    max_val = max(max_val)

    return puzzles, max_val


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

    puzzles, highest_num = readPuzzle(args.file, puzzle_rows, puzzle_cols)    
    root = Node(None, 0, 0, puzzles[0])
    stop = False
    currNode = root

    #THIS IS FOR TESTING PURPOSES
    #Keeps looping until "y" is input at end of round
    #chooses a random node in the list of children
    while not stop:
        print("Current board:")
        printBoard(currNode.board)
        children = buildChildren(currNode)
        
        goal1,goal2 = generate_goal(highest_num,puzzle_rows,puzzle_cols)
        
        man_dist1, man_distd2 = manhattan_distance(currNode.board,goal1,goal2)  #h1
        
        sum_per_inv1, sum_per_inv2 = sum_permutation_inversions(currNode.board,goal1,goal2) #h2

        for c in children:
            print("New board: ")
            printBoard(c.board)
            sum_per_inv1, sum_per_inv2 = sum_permutation_inversions(c.board,goal1,goal2) #h2

        value = input("stop generating? y/n ")

        if value.lower() == "y":
            stop = True
        else:
            print("----------NEXT ROUND----------")
            currNode = children[random.randint(0, len(children)-1)]

def run2():
    args = getArgs()

    puzzles, highest_num = readPuzzle(args.file, puzzle_rows, puzzle_cols)    
    root = Node(None, 0, 0, puzzles[2])
    #root = Node(None, 0, 0, np.array([[1,0,4,3],[5,2,6,7]]))
    stop = False
    currNode = root

    #THIS IS FOR TESTING PURPOSES
    #Keeps looping until "y" is input at end of round
    #chooses a random node in the list of children
    #while not stop:
        #print("Current board:")
        #printBoard(currNode.board)
    goal1,goal2 = generate_goal(highest_num,puzzle_rows,puzzle_cols)
        
    time, path = A_star(currNode,goal1,goal2, 2) #test1 with manhattan

    for n in path:
        print("--------------------")
        printBoard(n.board)
        print("Cost:", n.cost, "Total cost:", n.getTotalCost())

    print("Execution time:", round(time, 2), "seconds.")

        #value = input("stop generating? y/n ")

        #if value.lower() == "y":
        #    stop = True
        #else:
            #print("----------NEXT ROUND----------")

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
    run2()