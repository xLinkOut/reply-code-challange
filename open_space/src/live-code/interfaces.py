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