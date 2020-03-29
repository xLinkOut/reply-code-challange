# -*- coding: utf-8 -*-
from sys import argv
from json import dumps
from os.path import exists
import interfaces 

try:
    input_filename = argv[1]
    if not exists(input_filename):
        raise FileNotFoundError
except IndexError:
    exit("Missing input filename!")
except FileNotFoundError:
    exit("Input file not found!")

class Problem:
    def __init__(self,W,H):
        self.W = int(W)
        self.H = int(H)
        self.D = 0
        self.M = 0
        self.developers = dict()
        self.managers = dict()

    def set_num_developers(self,d):
        self.D = d
    
    def set_num_manager(self,m):
        self.M = m

with open(input_filename,'r') as input_file:
    
    # PARAMS
    first_line = input_file.readline().replace('\n','')
    global_parameters = first_line.split(' ')
    problem = Problem(*global_parameters)
    print(problem.W,problem.H)

    # MATRIX
    matrix = [[0 for x in range(problem.W)] for y in range(problem.H)] 
    for x in range(problem.H):
        row = input_file.readline().replace('\n','')
        print(row)
        for y in range(problem.W):
            matrix[x][y] = interfaces.Seat(row[y])
    print(matrix)
    # [['#', '#', '#', '#', '#'], ['#', '_', '#', '#', '_'], ['#', 'M', 'M', '_', '_']]

    # DEVELOPERS
    num_developers = input_file.readline().replace('\n','')
    problem.set_num_developers(int(num_developers))

    for d in range(problem.D):
        developer_data = input_file.readline().replace('\n','').split(' ')
        print(developer_data)
        developer = interfaces.Developer(d,developer_data[0],int(developer_data[1]),developer_data[3:])
        if developer_data[2] in problem.developers:
            problem.developers[developer_data[2]].append(developer)
        else:
            problem.developers[developer_data[2]] = [developer]

    print(problem.developers)

    # MANAGERS
    num_manager = input_file.readline().replace('\n','')
    problem.set_num_manager(int(num_manager))

    for m in range(problem.M):
        manager_data = input_file.readline().replace('\n','').split(' ')
        manager = interfaces.Manager(m,*manager_data)
        print(manager)
        if manager_data[0] in problem.managers:
            problem.managers[manager_data[0]].append(manager)
        else:
            problem.managers[manager_data[0]] = [manager]

    print(problem.managers)




    # End parsing
    # Magic happens here...
positioned = [] # list of positioned Replyer
for x in range(problem.H):
    print('')
    for y in range(problem.W):
        print(matrix[x][y].seat_type, end='')
        if matrix[x][y].seat_type == '_':
            if x < problem.H - 1:
                seat = matrix[x+1][y]
                if seat.seat_type == '_':
                    longest_skill_list = max(problem.developers.keys())
                    primo_dev = problem.developers[longest_skill_list][0]
                    print(primo_dev)
                    score = 0
                    max_index = 0
                    index = 1
                    for altri_dev in problem.developers[longest_skill_list][1:]:
                        local_score = primo_dev.work_potential(altri_dev) + primo_dev.bonus_potential(altri_dev)
                        if local_score > score:
                            score = local_score
                            max_index = index
                        index +=1
                    print(score,max_index)
                    print(primo_dev.skills)
                    print(problem.developers[longest_skill_list][max_index].skills)
                    seat.replyer = problem.developers[longest_skill_list].pop(max_index)
                    matrix[x][y].replyer = problem.developers[longest_skill_list].pop(0)
                    matrix[x][y].replyer.set_position(x, y)
                    seat.replyer.set_position(x+1, y)
                    positioned.append(seat.replyer)
                    positioned.append(matrix[x][y].replyer)
                    if len(problem.developers[longest_skill_list]) == 0:
                        problem.developers.pop(longest_skill_list)
            
            print(problem.developers.keys())

            if y < problem.W - 1:
                right_seat = matrix[x][y+1]
                if right_seat.seat_type == '_':
                    #print(problem.developers.keys())
                    longest_skill_list = max(problem.developers.keys())
                    primo_dev = right_seat.replyer if right_seat.replyer else problem.developers[longest_skill_list][0]
                    #print(primo_dev)
                    score = 0
                    max_index = 0
                    index = 1
                    for altri_dev in problem.developers[longest_skill_list][1:]:
                        print(primo_dev.skills)
                        print(altri_dev.skills)
                        local_score = primo_dev.work_potential(altri_dev) + primo_dev.bonus_potential(altri_dev)
                        if local_score > score:
                            score = local_score
                            max_index = index
                        index +=1
                    print(score,max_index)
                    if right_seat.replyer == None:
                        right_seat.replyer = primo_dev
                        primo_dev.set_position(x, y+1)
                        positioned.append(primo_dev)
                        
                    
                    matrix[x][y].replyer = problem.developers[longest_skill_list][max_index]
                    matrix[x][y].replyer.set_position(x, y)
                    positioned.append(matrix[x][y].replyer)

                    problem.developers[longest_skill_list].pop(0)
                    problem.developers[longest_skill_list].pop(max_index-1)
i = 0
for dev in sorted(positioned, key=lambda x: x.original_position):
    if dev.original_position != i:
        for j in range(dev.original_position - i):
            i += 1
            print("X")
    i += 1
    print(f"{dev.y} {dev.x}")