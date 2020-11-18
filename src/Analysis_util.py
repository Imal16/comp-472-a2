# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 14:00:29 2020

@author: Ihsaan
"""
import csv
import os
import numpy as np
from pathlib import Path
analysis_path = Path("../analysis2.4/")

def search_reader(algo,h=None,files=50,row=2,col=4):
    output_file = '{}-{}_searchcount.txt'.format(algo,h)
    line_count = []
    
    for i in range(files):
        if h==None:
            fname = "{}_{}_search.txt".format(i,algo)
        else:           
            fname = "{}_{}-{}_search.txt".format(i,algo,h)
        #print(fname)
        with open(analysis_path/fname) as f:
            for i, l in enumerate(f):
                pass
            last_line = l
            #print(last_line)
            if last_line == 'no solution':
                pass
            else:
                line_count.append(i)
    #print("Search_Length: ",line_count)
    print("Search Length average:", np.average(line_count))
    print("Search Length std dev:" , np.std(line_count))
    print("Search Length min:" , min(line_count))
    print("Search Length max:" , max(line_count))
    print("Search Length total:", sum(line_count))
# =============================================================================
#     
#     with open(analysis_path/output_file, 'w') as file:        
#         file.writelines(line_count)          #writelines takes an iterable and takes care of everything
# =============================================================================
        
    return 0

def solution_reader(algo,h=None,files=50,row=2,col=4):
    search_cost=[]
    search_time=[]
    No_solution=0
    output_file1 = '{}-{}_solcount.txt'.format(algo,h)
    output_file2 = '{}-{}_soltime.txt'.format(algo,h)
    
    
    for i in range(files):
        last_line=[]
        if h==None:
            fname = "{}_{}_solution.txt".format(i,algo)
        else:           
            fname = "{}_{}-{}_solution.txt".format(i,algo,h)
        #print(fname)
        with open(analysis_path/fname) as f:
            for line in f:
                pass
            last_line = line
            if last_line == 'no solution':
                No_solution+=1
            else:
                last_line = list(last_line.split("\t"))
                search_cost.append(int(last_line[0]))
                search_time.append(float(last_line[1]))
                
    #print("Solution Costs: ", search_cost)
    print("Solution Costs average:", np.average(search_cost))
    print("Solution Costs std dev:" , np.std(search_cost))
    print("Solution Cost total:", sum(search_cost))
    print("Solution Costs min:", min(search_cost))
    print("Solution Costs max:", max(search_cost))
    

    #print("Solution Times ",search_time)
    print("Solution Times average:", np.average(search_time))
    print("Solution Times std dev:" , np.std(search_time))
    print("Solution Time total:", sum(search_time))
    print("Solution Times min:", min(search_time))
    print("Solution Times max:", max(search_time))
    print("Amount of No Solutions: ", No_solution)
# =============================================================================
#         
#     with open(analysis_path/output_file1, 'w') as file:        
#         file.writelines(search_cost)          #writelines takes an iterable and takes care of everything
#         
#     with open(analysis_path/output_file2, 'w') as file:        
#         file.writelines(search_time)          #writelines takes an iterable and takes care of everything
# =============================================================================
        
        
    return 0






print("-----A STAR------H1-----")
search_reader('astar','h1',50)
solution_reader('astar','h1',50)


print("-----A STAR------H2-----")
search_reader('astar','h2',50)
solution_reader('astar','h2',50)

print("-----GBFS------H1-----")
search_reader('gbfs','h1',50)
solution_reader('gbfs','h1',50)


print("-----GBFS------H2-----")
search_reader('gbfs','h2',50)
solution_reader('gbfs','h2',50)


print("-----UCS-----")
search_reader('ucs',files=50)
solution_reader('ucs',files=50)