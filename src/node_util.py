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
    #viewing the board as x by y matrix
    y_max = len(node.board)-1
    x_max = len(node.board[0])-1
    zero = node.zero_coords #(node.zero_coords[1], node.zero_coords[0])
    #print('board', node.board)
    #print('zero',zero)
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
    
    #print('diagonals',new_zeros)

    #for nz in new_zeros:
    #    b = np.copy(node.board)
    #    b[nz[0], nz[1]], b[zero[0], zero[1]] = b[zero[0], zero[1]], b[nz[0], nz[1]]     #swapping: a,b = b,a
    #    moves.append(Node(node, node.depth+1, 3, b, nz))

    addMoves(moves, new_zeros, node, 3)
    
    #print('initial moves',moves)

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

    #print('wrap zero',new_zeros)
    
    addMoves(moves, new_zeros, node, 2)
    
    #print(moves)
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
        #print("New board: ")
        #printBoard(m.board)

    return moves