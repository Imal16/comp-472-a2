import csv
import argparse

from node import Node
from pathlib import Path

puzzle_folder = Path("../puzzles/")


#Placeholder for a method that takes in a node (any node) and generates its immediate children
#Maybe we could make a tree class, idk.
def buildChildren(node):
    pass


#reads the given pizzle file
#returns a list of puzzles
def readPuzzle(file):
    puzzles = []

    with open(puzzle_folder / file) as csvFile:
        reader = csv.reader(csvFile, delimiter=' ')
        
        for row in reader:
            p = []

            #Entries are read as characters by default...need to iterate over each and read as int
            for entry in row:
                p.append(int(entry))

            puzzles.append(p)

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

    puzzles = readPuzzle(args.file)

    print(puzzles)
    
    #Each algorithm needs to be run on each puzzle
    for p in puzzles:
        root = Node(None, 0, p)
 
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