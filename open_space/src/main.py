# -*- coding: utf-8 -*-
from json import dumps
#import interfaces 

from enum import Enum

class SeatType(Enum):
    UNAVAILABLE = '#'
    MANAGER     = 'M'
    DEVELOPER   = '_'

class Seat:
    def __init__(self, seat_type):
        self.seat_type = seat_type
        self.replyer = None
    
    def set_replyer(self, replyer):
        self.replyer = replyer

class Replyer:
    def __init__(self, original_position, company, bonus):
        self.original_position = original_position
        self.company = company
        self.bonus = bonus
        self.x = -1
        self.y = -1

    def is_positioned(self):
        return self.x != -1 #check only one position since the other must be set together

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def above(self, floor):
        if self.x == 0:
            return None
        return floor[self.x -1][self.y]

    def left(self, floor):
        if self.y == 0:
            return None
        return floor[self.x][self.y - 1]

    def below(self, floor):
        if self.x >= len(floor):
            return None
        return floor[self.x + 1][self.y]
    
    def right(self, floor):
        if self.y >= len(floor[0]):
            return None
        return floor[self.x][self.y + 1]
    
    def bonus_potential(self, replyer):
        if replyer and self.company == replyer.company:
            return self.bonus * replyer.bonus
        return 0

    def total_bonus_potential(self, floor):
        if not self.is_positioned():
            return 0

        bp = self.bonus_potential(self.left(floor).replyer)
        bp += self.bonus_potential(self.right(floor).replyer)
        bp += self.bonus_potential(self.above(floor).replyer)
        bp += self.bonus_potential(self.below(floor).replyer)
        return bp
        
        
class Developer(Replyer): 
    def __init__(self, original_position, company, bonus, skills):
        super().__init__(original_position, company, bonus)
        self.skills = skills

    def work_potential(self, replyer):
        if isinstance(replyer, Developer):
            common = 0
            for skill in self.skills:
                if skill in replyer.skills:
                    common += 1
            return common * (len(self.skills) + len(replyer.skills) - common * 2)
        return 0

    def total_work_potential(self, floor):
        if not self.is_positioned():
            return 0

        wp = self.work_potential(self.left(floor).replyer)
        wp += self.work_potential(self.right(floor).replyer)
        wp += self.work_potential(self.above(floor).replyer)
        wp += self.work_potential(self.below(floor).replyer)
        return wp

    def total_potential(self, floor):
        return self.total_work_potential(floor) + self.total_bonus_potential(floor)

    
class Manager(Replyer):
    def __init__(self, original_position, company, bonus):
        super().__init__(original_position,company,bonus)
    
    def total_potential(self, floor):
        return self.total_bonus_potential(floor)

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