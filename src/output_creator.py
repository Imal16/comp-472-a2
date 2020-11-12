"""
Created on Tue Nov 10 15:55:12 2020

@author: Ihsaan Malek & Olivier Racette
"""


#makes file name from all the info passed to output functions. because the same code was written twice really.
def create_file_name(puzzle_num, algo, suffix, h_num=None):
    name = str(puzzle_num) + "_" + algo 
    
    if h_num is not None:
        name += "-h" + str(h_num) 
    
    name += "_" + suffix + ".txt" 

    return name


#creates and outputs the solution data to the proper file. overwrites existing file.
def output_solution(output_file, sol_path, time, separator=" "):
    if(sol_path):
        #first, preparing output strings 
        lines = []
        total_cost = 0

        for n in sol_path:
            lines.append(str(n.token) + separator + str(n.cost) + separator + n.stringifyBoard(False))
            total_cost += n.cost

        lines.append(str(total_cost) + separator + str(round(time, 2)))

        #adding "\n" to every line
        lines = "\n".join(lines)
    else:
        lines = "No solution was found in " + str(time) + " seconds."
    

    #automatically overwrites existing files. file stream is also closed automatically. bless python!
    with open(output_file, 'w') as file:        
        file.writelines(lines)          #writelines takes an iterable and takes care of everything

    print("Wrote solution file.")


#creates and outputs the search data to the proper file. overwrites existing file.
def output_search(output_file, closed, separator=" "):
    lines = []

    for n in closed:
        lines.append(str(n.total_cost) + separator + str(n.root_cost) + separator + str(n.goal_cost) + separator + n.stringifyBoard(False))

    lines = "\n".join(lines)

    with open(output_file, 'w') as file:        
        file.writelines(lines)

    print("Wrote search file.")