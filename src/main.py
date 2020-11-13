# By Ihsaan Malek and Olivier Racette
# The goal of this program is to use several search algorithms (UCS, GBFS, A*) to complete an x-puzzle.

#python libraries
import csv
import argparse
import random
from pathlib import Path

#External dependencies
import numpy as np

#user imports
from node import Node
from node_util import buildChildren
from Search_functions import generate_goal, manhattan_distance, sum_permutation_inversions, search, cost_from_root, h0
from output_creator import output_solution, output_search, create_file_name


puzzle_folder = Path("../puzzles/")
output_path = Path("../output/")

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
    parser.add_argument("-t", "--timeout" ,type=int, help="Number of seconds before the search functions are timed out.", default=60)

    return parser.parse_args()


#Shows relevant information in console, such as solution path and execution time.
def printSolution(path, time):
    if path:
        cost = 0
        print("----------SOLUTION PATH----------")
        for n in path:    
            print(n.stringifyBoard(True))
            print("Cost:", n.cost, "\tg(n) =", n.root_cost, "\th(n) =", n.goal_cost, "\tf(n) = ", n.total_cost, "\tToken:", n.token)
            cost += n.cost
            print("---------- ----------")
        print("Execution time:", round(time, 2), "seconds.")
        print("Total path cost: ", cost)
    else:
        print("Failed to find a solution in %i seconds." %time)


#Each algorithm needs to be run on each puzzle
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
def run():
    args = getArgs()

    puzzles, highest_num = readPuzzle(args.file, puzzle_rows, puzzle_cols)
    goal1,goal2 = generate_goal(highest_num,puzzle_rows,puzzle_cols)

    algos = ["ucs", "gbfs", "astar"]

    for i in range(len(puzzles)):        #we need the puzzle index for some parts of the code
        print("----------NEW PUZZLE----------")

        root = Node(None, 0, 0, puzzles[i])  

        for a in algos:
            print("Finding solution with " + a + "...")

            if a == "ucs":
                heuristics = {-1: lambda x, y, z: (0,0)}
            else:
                heuristics = {
                    1: sum_permutation_inversions,
                    2: manhattan_distance
                }

            if a == "gbfs":
                gn = lambda x: 0
            else:
                gn = cost_from_root

            for h_num, h in heuristics.items():
                time, path, closed = search(root, goal1, goal2, gn, h, args.timeout)
                #printSolution(path, time)

                #note that tabs are being used as seperators instead of spaces to make it easier to read. can be undone by removing separator param un both output functions.
                file_name = create_file_name(i, a, "solution", h_num)
                output_solution(output_path/file_name, path, time, separator="\t")

                file_name = create_file_name(i, a, "search", h_num)
                output_search(output_path/file_name, closed, separator="\t")

    print("Execution complete.")
            

if __name__ == "__main__":
    run()