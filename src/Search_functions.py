# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:28:39 2020

@author: Ihsaan Malek and Olivier Racette
"""
'''
goal can be  [[1,2,3,4],[5,6,7,0]] or [[1,3,5,7],[2,4,6,0]] <- increases as you go down the column
'''
import numpy as np
import heapq 
from collections import deque
import time
from node_util import buildChildren



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
    

def diagonal_check(zero, curr_coords, goal_coords, x_max, y_max):
    upper_left = (0, 0)
    upper_right = (0, x_max)
    lower_left = (y_max, 0)
    lower_right = (y_max, x_max)

    if goal_coords == zero:     #common condition, took it out
        if zero == upper_left and (curr_coords == lower_right or curr_coords == (zero[0]+1, zero[1]+1)):
            return True

        elif zero == upper_right and (curr_coords == lower_left or curr_coords == (zero[0]+1, zero[1]-1)):
            return True

        elif zero == lower_left and (curr_coords == upper_right or curr_coords == (zero[0]-1, zero[1]+1)):
            return True

        elif zero == lower_right and (curr_coords == upper_left or curr_coords == (zero[0]-1, zero[1]-1)):
            return True

    return False


def wrap_check(zero, curr_coords, goal_coords, x_max, y_max):
    if goal_coords == zero:     #common condition, took it out
        if zero[1] == 0 and curr_coords[1] == x_max and curr_coords[0] == zero[0]:
            return True
        elif zero[1] == x_max and curr_coords[1] == 0 and curr_coords[0] == zero[0]:
            return True

        #can only do vertical wrapping if the board has more than 2 rows
        if y_max > 1:
            if zero[0] == 0 and curr_coords[0] == y_max and curr_coords[1] == zero[1]:
                return True
            elif zero[0] == y_max and curr_coords[0] == 0 and curr_coords[1] == zero[1]:
                return True

    return False


def manhattan_distance(node, goal_state1,goal_state2):
    #re-write to take diags and wrap around into account
    #if goal_coords is on a border and 0 is on the opposite side
    # dist = 1
    #if 0 is in a corner and goal_coords is place for diag move:
    # dist = 1
    board = node.board 
    distance1, distance2 = 0,0
    zero = node.zero_coords
    y_max = len(node.board)-1
    x_max = len(node.board[0])-1

    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            curr_coords = (i, j)

            goal_coords1 = np.where(goal_state1 == board[i][j])
            x1, y1 = goal_coords1[0], goal_coords1[1] 

            if diagonal_check(zero, curr_coords, goal_coords1, x_max, y_max) or wrap_check(zero, curr_coords, goal_coords1, x_max, y_max):
                distance1 += 1
            else:
                distance1 += sum(abs(i-x1),abs(j-y1))[0]


            goal_coords2 = np.where(goal_state2 == board[i][j])
            x2, y2 = goal_coords2[0], goal_coords2[1]

            if diagonal_check(zero, curr_coords, goal_coords2, x_max, y_max) or wrap_check(zero, curr_coords, goal_coords2, x_max, y_max):
                distance2 += 1
            else:
                distance2 += sum(abs(i-x2),abs(j-y2))[0]

    #print('Solution 1 est. cost: {}, Solution 2 est. cost: {}\n'.format(distance1[0], distance2[0]))
    
    return distance1, distance2

def sum_permutation_inversions(node, goal_state1,goal_state2):
    board = node.board
    distance1, distance2 = 0,0
    temp_board1 = board.reshape(board.shape[0]*board.shape[1]) #flatten to 1d array
    
    goal_state2= goal_state2.reshape(board.shape[0]*board.shape[1])
    temp_board2 = board.reshape(board.shape[0]*board.shape[1]) #flatten to 1d array
    
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            #print(board[i][j])
            #print(i,j)
            #goal 1
            #reimagin the matrix as a singylar ordered array [1,2...,n-1]
            #the position/index of element i should be i-1 in the reimagined goal array
            #5 should be in slot 4, 
            
            current_coords1 = np.where(temp_board1 == board[i][j])
            
            if board[i][j] == 0:
                distance1 += abs(current_coords1[0]-(board.shape[0]*board.shape[1]-1)) #special case, 0 should be in the last spot, index of n-1
            else:
                 distance1 += abs(board[i][j]-1-current_coords1[0])
                
                
            #print('d1: ',distance1 )
            
            #goal 2
            
            
            goal_coords2 = np.where(goal_state2 == board[i][j])
            current_cord2 = np.where(temp_board2 == board[i][j])
            
            distance2 += abs(goal_coords2[0]-current_cord2[0])
            #print('d2: ',distance2 )
    
    #print('Solution 1 est. cost: {}, Solution 2 est. cost: {}\n'.format(distance1, distance2[0]))
    
    return distance1[0], distance2[0]

def h0(board, goal_state1,goal_state2):
    
    if board[board.shape[0]-1][board.shape[1]-1] == 0:
        distance1 = distance2 = 0
        return distance1, distance2
    else:
        distance1 = distance2 = 1
        return distance1, distance2


def check_goal(board, goal_state1,goal_state2):
    #using all() saves a few ms. why???
    #if np.array_equal(board,goal_state1):
    if (board == goal_state1).all():
        return (True, 1)
        
    #elif np.array_equal(board,goal_state2):
    elif (board == goal_state2).all():
        return (True, 2)
        
    else:
        return (False, 0)
    
#returns total cost from node to root
#This was compared to a non-recursive method and it was the same execution time
def cost_from_root(n):
    if n is None:
        return 0
    else:
        return n.cost + cost_from_root(n.parent)

#returns a list of nodes from the root to the passed node
def getPath(n):
    currNode = n
    path = []

    while currNode is not None:
        path.append(currNode)
        currNode = currNode.parent

    path.reverse()  #reverse works in place!

    return path
    
def heuristic(number,board,goal_state1,goal_state2):
    if number == 0:
        return h0(board, goal_state1,goal_state2)
    elif number == 1:
        return manhattan_distance(board, goal_state1,goal_state2)
    elif number == 2:
        return sum_permutation_inversions(board, goal_state1,goal_state2)
    else:
        raise Exception('Please enter a value between 0-2')
        

 
def search(StartNode, goal1, goal2, g, h, max_time):
    '''
    Used Algorithm from slide set 3.7, page 7
    '''
    openlist = []
    closedlist = deque()
    path = []
    current_node = StartNode
    reached_goal = False
    #goalstate = 0 
    
    heapq.heappush(openlist, current_node) #insert root node into heaph

    stop_time = 0
    start_time = time.time()

    while openlist and (time.time() - start_time) < max_time: 
        
        current_node = heapq.heappop(openlist)  #popheap
    
        reached_goal, goalstate = check_goal(current_node.board,goal1,goal2)        #goalstate is not used

        if reached_goal:   #goal is reached, trigger flag to exit while
            print("----------SUCCCESS----------")
            stop_time = (time.time() - start_time)
            path = getPath(current_node)
            return stop_time, path, closedlist

        children = buildChildren(current_node)

        for child in children:        
            child.root_cost = g(child)
            h_cost1, h_cost2 = h(child, goal1, goal2)
            child.goal_cost = min(h_cost1, h_cost2)
            child.total_cost = child.root_cost + child.goal_cost
            
            #use space, but mkaes finding index faster due to np vectorization
            temp_close = np.array([c.board for c in closedlist])
            
            try:#if child exist in closed
                
                closed_same_child_index = np.where(np.all(np.all(temp_close == child.board,axis=2),axis=1))[0][0]
                closed_child_cost = closedlist[closed_same_child_index].total_cost #get cost of that state

                if closed_child_cost > child.total_cost: #if new path is lower
                    heapq.heappush(openlist, child) #push into open, need to revisit
                        
            except: #not in closed, check open
                
                try: #check if in open
                    del temp_close
                    temp_open = np.array([c.board for c in openlist]) # creates an np.array containing all board states from open list

                    open_same_child_index = np.where(np.all(np.all(temp_open == child.board,axis=2),axis=1))[0][0]
                    #child exists in open
                    current_child_cost = openlist[open_same_child_index].total_cost #get cost of that state
                    
                    if current_child_cost > child.total_cost: #if new path is cheaper, replace cost value
                        openlist[open_same_child_index][0] = child.total_cost
                        heapq.heapify(openlist)

                except: #if not in open or closed, just push.
                        heapq.heappush(openlist, child) #crrent children stored in heap  by order of cost

        closedlist.append(current_node)

    print("----------FAILURE----------")    
    return max_time, [], []