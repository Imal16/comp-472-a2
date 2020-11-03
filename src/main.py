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

    #Sample node
    root = Node(None, 0, [3,0,1,4,2,6,5,7])     #numbers taken from the first sample puzzle

    print(root.__doc__)
    print(root.__dict__)

    puzzles = readPuzzle(args.file)

    print(puzzles)


if __name__ == "__main__":
    run()