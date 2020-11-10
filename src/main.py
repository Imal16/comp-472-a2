# By Ihsaan Malek and Olivier Racette
# The goal of this program is to use several search algorithms (UCS, GBFS, A*) to complete an x-puzzle.

import csv
import argparse
import random
import time
import heapq

#External dependencies
import numpy as np

from node import Node
from pathlib import Path
from queue import PriorityQueue


puzzle_folder = Path("../puzzles/")

#Leaving this here for now. Would be great if it wasn't hard coded but we don't really have a way of doing it another way with the data format.
#We can't really infer the dimensions of the puzzle from the txt file
#8 puzzle is supposed to be 3x3 grid, but our version has 8-puzzle being 2x4 grid...
puzzle_rows = 2
puzzle_cols = 4

#Makes Node objects from a series of (y, x) tuples that represent coordinates of the "zero" tile and adds them to the passed movesList
def addMoves(moves_list, zeros, parent, cost):
    zero = parent.zero_coords

    for z in zeros:
        b = np.copy(parent.board)
        b[z[0], z[1]], b[zero[0], zero[1]] = b[zero[0], zero[1]], b[z[0], z[1]]     #swapping: a,b = b,a
        moves_list.append(Node(parent, parent.depth+1, cost, b, z))   


#Method that takes in a node (any node) and generates its immediate children
# Legal moves:
#   direct horizontal / vertical translation (cost 1)
#   wrapping horizontal / vertical translation (cost 2) NOTE: vertical wrapping is only OK when there are more than 2 rows
#   diagonal (direct or wrap) (cost 3)
def buildChildren(node):
    #viewing the board as x by y matrix
    y_max = len(node.board)-1
    x_max = len(node.board[0])-1
    zero = node.zero_coords #(node.zero_coords[1], node.zero_coords[0])

    #NOTE that x and y are inverted for all tuples
    upper_left = (0, 0)
    upper_right = (0, x_max)
    lower_left = (y_max, 0)
    lower_right = (y_max, x_max)

    #building a list of moves that are possible
    moves = []

    new_zeros = []

    #cases where diagonal movement is permitted
    if zero == upper_left:
        #print("0 at: upper left") 
        #can go directly diagonal lower right or wrap diagonal with last value in board
        new_zeros.append((zero[0] + 1, zero[1] + 1))
        new_zeros.append((zero[0] + 1, x_max))

    elif zero == upper_right:
        #print("0 at upper right")
        #can go to immediate diagonal lower right or wrap diagonal lower left
        new_zeros.append((zero[0] + 1, zero[1] - 1))
        new_zeros.append((zero[0] + 1, 0))

    elif zero == lower_left:
        #print("0 at: lower left")
        #can go to immediate diagonal upper right or wrap diagonal upper left
        new_zeros.append((zero[0] - 1, zero[1] + 1))
        new_zeros.append((zero[0] - 1, x_max))

    elif zero == lower_right:
        #print("0 at: lower right")
        #can go to immediate diagonal upper left or wrap diagonal upper right
        new_zeros.append((zero[0] - 1, zero[1] - 1))
        new_zeros.append((zero[0] - 1, 0))


    #for nz in new_zeros:
    #    b = np.copy(node.board)
    #    b[nz[0], nz[1]], b[zero[0], zero[1]] = b[zero[0], zero[1]], b[nz[0], nz[1]]     #swapping: a,b = b,a
    #    moves.append(Node(node, node.depth+1, 3, b, nz))

    addMoves(moves, new_zeros, node, 3)


    #cases where wrap-around is permitted
    #wrapping horizontal / vertical translation (cost 2) NOTE: vertical wrapping is only OK when there are more than 2 rows

    new_zeros = []

    if zero[1] == 0:
        new_zeros.append((zero[0], x_max))
    elif zero[1] == x_max:
        new_zeros.append((zero[0], 0))

    #can only do vertical wrapping if the board has more than 2 rows
    if y_max > 1:
        if zero[0] == 0:
            new_zeros.append((y_max, zero[1]))
        elif zero[0] == y_max:
            new_zeros.append((0, zero[1]))


    addMoves(moves, new_zeros, node, 2)

    #cases with simple translation
    new_zeros = []

    if zero[1] < x_max:
        new_zeros.append((zero[0], zero[1] + 1))
    
    if zero[1] > 0:
        new_zeros.append((zero[0], zero[1] - 1))

    if zero[0] > 0:
        new_zeros.append((zero[0] - 1, zero[1]))
    
    if zero[0] < y_max:
        new_zeros.append((zero[0] + 1, zero[1]))

    addMoves(moves, new_zeros, node, 1)

    #for m in moves:
    #    print("New board: ")
    #    printBoard(m.board)

    return moves


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


#Printing the puzzle board without the brackets...
def printBoard(board):
    for row in board:
        print(*row, sep=' ')


#returns total cost from node to root
#This was compared to a non-recursive method and it was the same execution time
def g(n):
    if n is None:
        return 0
    else:
        return n.cost + g(n.parent)

#returns a list of nodes from the root to the passed node
def getPath(n):
    currNode = n
    path = []

    while currNode is not None:
        path.append(currNode)
        currNode = currNode.parent

    path.reverse()  #reverse works in place!

    return path


def run():
    args = getArgs()

    puzzles = readPuzzle(args.file, puzzle_rows, puzzle_cols)
    
    #s = Node(None, 0, 0, np.array([[1,0,4,3],[5,2,6,7]]) )
    s = Node(None, 0, 0, puzzles[2])
    op = [] #PriorityQueue()
    closed = []

    g1 = [[1,2,3,4],[5,6,7,0]]
    g2 = [[1,3,5,7],[2,4,6,0]]

    heapq.heappush(op, s)

    start_time = time.time()
    max_time = 60
    stop_time = 0
    round_count = 1

    success = False

    while op and (time.time() - start_time) < max_time:
        round_timer = time.time()
        s = heapq.heappop(op)

        if (s.board == g1).all() or (s.board == g2).all():  #success!
            print("----------SUCCCESS----------")
            stop_time = (time.time() - start_time)
            success = True
            break
        else:
            closed.append(s)
            children = buildChildren(s)

            for c in children:
                c.root_cost = g(c)

                #if c is already in open and its more expensive, we need to swap it
                for i in range(len(op)):
                    if c == op[i] and c < op[i]:
                        op[i] = c
                        break;
                
                if c not in closed:
                    heapq.heappush(op, c)

        #print("Round", round_count, len(op), len(closed), "Time:", round((time.time() - round_timer),3))
        round_count += 1

    if success:
        path = getPath(s)

        for n in path:
            print("--------------------")
            printBoard(n.board)
            print("Cost:", n.cost, "Total cost:", n.root_cost)

        print("Execution time:", stop_time)
    else:
        print("Failed to find a solution in %i seconds." %max_time)

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