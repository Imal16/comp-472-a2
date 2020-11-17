# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:55:12 2020

@author: Ihsaan Malek & Olivier Racette
"""
from node import Node
import numpy as np

#Makes Node objects from a series of (y, x) tuples that represent coordinates of the "zero" tile and adds them to the passed movesList
def addMoves(moves_list, zeros, parent, cost):
    zero = parent.zero_coords

    for z in zeros:
        b = np.copy(parent.board)
        b[z[0], z[1]], b[zero[0], zero[1]] = b[zero[0], zero[1]], b[z[0], z[1]]             #swapping: a,b = b,a         
        moves_list.append(Node(parent, parent.depth+1, cost, b, z, b[zero[0], zero[1]]))    #for the token that was moved: it was just swapped with 0!


#Method that takes in a node (any node) and generates its immediate children
# Legal moves:
#   direct horizontal / vertical translation (cost 1)
#   wrapping horizontal / vertical translation (cost 2) NOTE: vertical wrapping is only OK when there are more than 2 rows
#   diagonal (direct or wrap) (cost 3)
def buildChildren(node):
    #viewing the board as y by x matrix
    y_max = len(node.board)-1
    x_max = len(node.board[0])-1
    zero = node.zero_coords 

    #NOTE that x and y are inverted for all tuples (array[y][x])
    upper_left = (0, 0)
    upper_right = (0, x_max)
    lower_left = (y_max, 0)
    lower_right = (y_max, x_max)

    #building a list of moves that are possible
    all_moves = []

    cost_1_moves = []
    cost_2_moves = []
    cost_3_moves = []

    #cases where the 0 tile is at the diagonals
    if zero == upper_left:
        #can go directly diagonal lower right or wrap diagonal with last value in board
        cost_3_moves.append((zero[0] + 1, zero[1] + 1))
        cost_3_moves.append((zero[0] + 1, x_max))

        #can also wrap around with the tile at the other end, either horizontally or vertically (if there are more than 2 rows) 
        cost_2_moves.append((zero[0], x_max))

        if y_max > 1:
            cost_2_moves.append((y_max, zero[1]))

    elif zero == upper_right:
        #can go to immediate diagonal lower right or wrap diagonal lower left
        cost_3_moves.append((zero[0] + 1, zero[1] - 1))
        cost_3_moves.append((zero[0] + 1, 0))

        #wrap around
        cost_2_moves.append((zero[0], 0))

        if y_max > 1:
            cost_2_moves.append((y_max, zero[1]))

    elif zero == lower_left:
        #print("0 at: lower left")
        #can go to immediate diagonal upper right or wrap diagonal upper left
        cost_3_moves.append((zero[0] - 1, zero[1] + 1))
        cost_3_moves.append((zero[0] - 1, x_max))

        #wrap around
        cost_2_moves.append((zero[0], x_max))

        if y_max > 1:
            cost_2_moves.append((0, zero[1]))

    elif zero == lower_right:
        #print("0 at: lower right")
        #can go to immediate diagonal upper left or wrap diagonal upper right
        cost_3_moves.append((zero[0] - 1, zero[1] - 1))
        cost_3_moves.append((zero[0] - 1, 0))

        #wrap around
        cost_2_moves.append((zero[0], 0))

        if y_max > 1:
            cost_2_moves.append((0, zero[1]))


    #cases with simple translation
    if zero[1] < x_max:
        cost_1_moves.append((zero[0], zero[1] + 1))
    
    if zero[1] > 0:
        cost_1_moves.append((zero[0], zero[1] - 1))

    if zero[0] > 0:
        cost_1_moves.append((zero[0] - 1, zero[1]))
    
    if zero[0] < y_max:
        cost_1_moves.append((zero[0] + 1, zero[1]))

    #I had to patch this at the last minute because I didn't code the rules properly!! Code could be better but eh it works.
    addMoves(all_moves, cost_1_moves, node, 1)
    addMoves(all_moves, cost_2_moves, node, 2)
    addMoves(all_moves, cost_3_moves, node, 3)

    return all_moves