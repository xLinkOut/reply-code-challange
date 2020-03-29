# -*- coding: utf-8 -*-
from sys import argv
from os.path import exists

# Global
DEBUG = True

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
        self.W = int(W) # Width  (X axis) (column)
        self.H = int(H) # Height (Y axis) (row)
        self.D = 0 # Num of Developers
        self.M = 0 # Num of Profect Manager
        self.developers = list()
        self.managers = list()

    def set_num_developers(self,d):
        self.D = d
    
    def set_num_managers(self,m):
        self.M = m

    def add_developer(self, company, bonus, skills):
        self.developers.append({
            "company": company,
            "bonus": bonus,
            "skills": skills
        })

    def add_manager(self, company, bonus):
        self.managers.append({
            "company": company,
            "bonus": bonus
        })

# PARSER
with open(input_filename,'r') as input_file:
    
    # PARAMS (W,H)
    first_line = input_file.readline().replace('\n','')
    global_parameters = first_line.split(' ')
    problem = Problem(*global_parameters)
    if DEBUG: print(problem.W,problem.H)

    # MAP
    space = [[0 for x in range(problem.W)] for y in range(problem.H)] 
    for row in range(problem.H):
        line = input_file.readline().replace('\n','')
        for column in range(problem.W):
            space[row][column] = line[column]
    if DEBUG: print(space)

    # DEVELOPERS
    num_developers = input_file.readline().replace('\n','')
    problem.set_num_developers(int(num_developers))
    for row in range(problem.D):
        line = input_file.readline().replace('\n','').split(' ')
        problem.add_developer(line[0],int(line[1]),line[3:])
    if DEBUG: print(problem.developers)

    # PROJECT MANAGERS
    num_manager = input_file.readline().replace('\n','')
    problem.set_num_managers(int(num_manager))

    for row in range(problem.M):
        line = input_file.readline().replace('\n','').split(' ')
        problem.add_manager(line[0],int(line[1]))
    if DEBUG: print(problem.managers)

# Magic happens here...

for row in range(problem.H):
    for column in range(problem.W):
        if DEBUG: print(f"Posto attuale: {space[row][column]} ({row},{column})")
        if space[row][column] == '_': # Developer
            if row < problem.H - 1: # Se non sono all'ultima riga
                # Controllo sotto
                if space[row+1][column] == '_': # C'è un developer
                    pass
            if column < problem.W - 1: # Se non sono all'ultima colonna
                # Controllo a destra
                if space[row][column+1] == '_': # C'è un developer
                    pass