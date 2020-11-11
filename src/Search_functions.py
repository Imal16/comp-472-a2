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
import time
from node_util import buildChildren, printBoard



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
            
    #print('Solution 1 est. cost: {}, Solution 2 est. cost: {}\n'.format(distance1[0], distance2[0]))
    
    
    
    return distance1[0], distance2[0]

def sum_permutation_inversions(board, goal_state1,goal_state2):
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
    if np.array_equal(board,goal_state1):
        return (True, 1)
        
    elif np.array_equal(board,goal_state2):
        return (True, 2)
        
    else:
        return (False, 0)
    
#returns total cost from node to root
#This was compared to a non-recursive method and it was the same execution time

def g(n):           #error was thrown regarding parent.node ==Nonetype
    try:
        if n is None:
            return 0
        else:
            return n.cost + g(n.parent)
    except:
        return 0

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
        

 
def A_star(StartNode,goal1,goal2, h):
    '''
    Used Algorithm from slide set 3.7, page 7
    '''
    openlist = []
    closedlist = []
    path = []
    current_node = StartNode
    reached_goal = False
    goalstate = 0 
    solution_flag=0
    
    heapq.heappush(openlist, (0,current_node)) #insert root node into heaph

    max_time = 60
    stop_time = 0
    start_time = time.time()

    while openlist and (time.time() - start_time) < max_time: 
        
        current_node = heapq.heappop(openlist)[1]  #popheap
    
        #print("Current board:")
        #printBoard(current_node.board)
    
        reached_goal, goalstate = check_goal(current_node.board,goal1,goal2)

        if reached_goal == True:   #goal is reached, trigger flag to exit while
            #solution_flag = 1
            print("----------SUCCCESS----------")
            stop_time = (time.time() - start_time)
            path = getPath(current_node)
            break

        children = buildChildren(current_node)

        for child in children:
            close_flag=0
            open_flag = 0
            

            
            g_cost = g(child)
            h_cost1, h_cost2 = heuristic(h,child.board,goal1,goal2)
            total_cost = min(g_cost+h_cost1, g_cost+h_cost2)

            #print(total_cost)
            #if total_cost < 5: #debug
            #    print(child.board)
            
            #use space, but mkaes finding index faster due to np vectorization
            temp_close = np.array([c[1].board for c in closedlist])
            
            try:#if child exist in closed
                
                closed_same_child_index = np.where(np.all(np.all(temp_close == child.board,axis=2),axis=1))[0][0]
                closed_child_cost = closedlist[closed_same_child_index][0] #get cost of that state
                
                if closed_child_cost > total_cost: #if new path is lower
                    heapq.heappush(openlist, [total_cost,child]) #push into open, need to revisit
                    #print('child in closed')
                else:
                        #print('skip close')
                        close_flag = 1
                        
            except: #not in closed, check open
                
                try: #check if in open
                    del temp_close
                    temp_open = np.array([c[1].board for c in openlist]) # creates an np.array containing all board states from open list
                    #print("temporary OPE", temp_open)  
                    
                    open_same_child_index = np.where(np.all(np.all(temp_open == child.board,axis=2),axis=1))[0][0]
                    #child exists in open
                    #print('Index in open: ',open_same_child_index)
                    current_child_cost = openlist[open_same_child_index][0] #get cost of that state
                    
                    #print('cost in open:',current_child_cost)
                    #print('path_cost',total_cost)
                    
                    if current_child_cost > total_cost: #if new path is cheaper, replace cost value
                        #print('Open, there is a duplpppppp')
                        openlist[open_same_child_index][0] = total_cost
                        heapq.heapify(openlist)

                    else:
                        #print('skip open')
                        open_flag = 1 
                    
                except: #if not in open or closed, just push.
                        #print('NEW')
                        #if open_flag ==1 or close_flag ==1:
                            #print('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFffffffffffff errors')
                        #print(child.board)
                        heapq.heappush(openlist, [total_cost,child]) #crrent children stored in heap  by order of cost

                
        if solution_flag == 0:   
            heapq.heappush(closedlist, [0,current_node]) #insert original node into explored
            
            #current_node = heapq.heappop(openlist)[1] #pops the lowest cost node
            #print("LOL")
            #print("New board: ")
            #printBoard(current_node.board)
        
    
    #if solution_flag ==1:
    #    if goalstate != 1 or goalstate !=2:
    #        raise Exception('Error in bound') #double check goal condition
            
        #print('Goal Reached!')
        #print("New board: ")
        #printBoard(current_node.board)
        #if goalstate == 1:
        #    print(goal1)
        #if goalstate == 2:
        #    print(goal2)
        
    return stop_time, path
    
'''
for testing individual functions

goal =np.array([[1,2,3,4],[5,6,7,0]])
test1 =np.array([[1,2,3,4],[5,6,7,0]])
test2 = np.array([[1,2,3,4],[5,6,0,7]])
test3= np.array([[[1,2,3,4],[5,6,0,7]],[[2,1,3,4],[5,6,0,7]],[[1,2,3,4],[5,6,7,0]]])
print(np.where(np.all(np.all(test3 == goal,axis=2),axis=1))[0][0]) #gets index of same matrices. 

print(np.array([r[1] for r in test3]))

#print(np.where(np.all(test3==goal)))

goal1= np.array([[1,2,3,4],[5,6,7,0]])
goal2= np.array([[1,3,5,7],[2,4,6,0]])
cstate = np.array([[1,3,6,5],[2,4,0,7]])
cstate2 =np.array([[1,2,3,4],[5,6,7,0]])
print(sum_permutation_inversions(cstate,goal1,goal2))
print(manhattan_distance(cstate,goal1,goal2))
print(goal2.reshape(cstate.shape[0]*cstate.shape[1]))

rgoal, goalyes = check_goal(cstate2,goal1,goal2)
print(rgoal, goalyes)
'''