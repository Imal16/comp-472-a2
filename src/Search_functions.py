# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:28:39 2020

@author: Ihsaan Malek and Olivier Racette
"""
'''
goal can be  [[1,2,3,4],[5,6,7,0]] or [[1,3,5,7],[2,4,6,0]] <- increases as you go down the column
'''
import numpy as np

def generate_goal(highestnum,puzzle_rows,puzzle_cols):

    if highestnum+1 != puzzle_rows*puzzle_cols:
        
        raise Exception('Please revise puzzle, size or numbers are wrong')
    
    goal_state= np.append(np.arange(1,highestnum+1),[0])
    goal_state1 = goal_state.reshape(puzzle_rows,puzzle_cols)
    print('Goal State 1:\n',goal_state1)
    print('\n')
    
    
    goal_state2 = []
    first_index=1
    for i in range(puzzle_rows):
        row=np.arange(first_index,highestnum+1,puzzle_rows) #can implement vis np.arange(first_index, first_index*puzzle_row)then colstack
        goal_state2 = np.append(goal_state2,row)
        first_index += 1
        
    goal_state2 = np.append(goal_state2,0)
    goal_state2 = goal_state2.astype(int).reshape(puzzle_rows,puzzle_cols)
    print('Goal State 2:\n',goal_state2)
    print('\n')
    
    return (goal_state1, goal_state2)
    
#generate_goal(7,2,4)


def manhattan_distance(board, goal_state1,goal_state2):
    
    distance1, distance2 = 0,0

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            #print(board[i][j])
            #print(i,j)
            #goal 1
            goal_coords1 = np.where(goal_state1 == board[i][j])
            x1, y1 = goal_coords1[0], goal_coords1[1]
            distance1 += sum(abs(i-x1),abs(j-y1))
            #print('d1: ',distance1 )
            #goal 2
            goal_coords2 = np.where(goal_state2 == board[i][j])
            x2, y2 = goal_coords2[0], goal_coords2[1]
            distance2 += sum(abs(i-x2),abs(j-y2))
            #print('d2: ',distance2 )
            
    print(distance1, distance2)
    
    
    
    return distance1, distance2

def sum_permutation_inversions(board, goal_state1,goal_state2):
    distance1, distance2 = 0,0

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            #print(board[i][j])
            #print(i,j)
            #goal 1
            #reimagin the matrix as a singylar ordered array [1,2...,n-1]
            #the position/index of element i should be i-1 in the reimagined goal array
            #5 should be in slot 4, 
            if board[i][j] == 0:
                distance1 += abs((i+1)*j-(board.shape[0]*board.shape[1]-1)) #special case, 0 should be in the last spot, index of n-1
            else:
                distance1 += abs(board[i][j]-1-(i+1)*j)
                
            #print('d1: ',distance1 )
            
            #goal 2
            goal_state2= goal_state2.reshape(board.shape[0]*board.shape[1])
            goal_coords = np.where(goal_state2 == board[i][j])

            distance2 += abs(goal_coords[0]-(i+1)*j)
            #print('d2: ',distance2 )
    
    print(distance1, distance2)
    
    return distance1, distance2

def h0(board, goal_state1,goal_state2):
    
    if board[board.shape[0]-1][board.shape[1]-1] == 0:
        distance1 = distance2 = 0
        return distance1, distance2
    else:
        distance1 = distance2 = 1
        return distance1, distance2


