from Entities.vehicles import *
from Entities.floaters import *
from Entities.lilies import *
from Entities.frogs import *
from random import randint

class spriteGenerator():
    def __init__(self, size, screen_width, screen_height): 
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height

    def spawn_floaters(self, group, frog, friend_frog, level):
        log_small_x = randint(-self.size * 4, -self.size * 2)
        log_medium_x = randint(-self.size * 10, -self.size * 4)
        log_large_x = randint(-self.size * 8, -self.size * 3)
        turtle_medium_x = randint(self.size * 9, self.screen_width + self.size * 4)
        turtle_large_x = randint(self.size * 4, self.screen_width + self.size)
        log = Log('log_small', self.size, log_small_x)
        group.add(log)
        friend_frog.add(FriendFrog(self.size, frog, log))
        group.add(Log('log_small', self.size, log_small_x - self.screen_width / 3 - self.size))
        group.add(Log('log_small', self.size, log_small_x - 2 * self.screen_width / 3 - self.size))
        if level == 1:
            group.add(Log('log_medium', self.size, log_medium_x))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 6))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 11))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 16))
            group.add(Log('log_large', self.size, log_large_x))
            group.add(Log('log_large', self.size, log_large_x - self.size * 8))
            group.add(Log('log_large', self.size, log_large_x - self.size * 16))
            group.add(DivingTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 5))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 10))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 15))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 5))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 10))
            group.add(DivingTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 15))
        elif level == 2:
            group.add(Log('log_medium', self.size, log_medium_x))
            group.add(Crocodile(self.size, log_medium_x - self.size * 7))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 15))
            group.add(SnakeLog(self.size, log_large_x))
            group.add(Log('log_large', self.size, log_large_x - self.size * 10, 2))
            group.add(Log('log_large', self.size, log_large_x - self.size * 19, 2))
            group.add(DivingTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 5))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 10))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 15))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 5))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 10))
            group.add(DivingTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 15))
        elif level >= 3:
            group.add(Log('log_medium', self.size, log_medium_x))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 6))
            group.add(Crocodile(self.size, log_medium_x - self.size * 11))
            group.add(Log('log_medium', self.size, log_medium_x - self.size * 16))
            group.add(SnakeLog(self.size, log_large_x))
            group.add(Log('log_large', self.size, log_large_x - self.size * 10, 3))
            group.add(Log('log_large', self.size, log_large_x - self.size * 19, 3))
            group.add(DivingTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 5))
            group.add(NormalTurtle('turtle_medium', self.size, self.screen_width, turtle_medium_x + self.size * 13))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x))
            group.add(NormalTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 8))
            group.add(DivingTurtle('turtle_large', self.size, self.screen_width, turtle_large_x + self.size * 15))


    def spawn_vehicles(self, group, level):
        car_x = randint(self.size * 2, self.size * 8)
        racecar_x = randint(self.size * 2, self.size * 8)
        truck_x = randint(self.size * 6, self.size * 10)
        if level == 1:
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x))
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x + self.size * 10))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x - self.size * 7))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x + self.size * 10))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x  - self.size * 7))
            group.add(Vehicle('racecar2', self.screen_width, self.screen_height, self.size, racecar_x))
        elif level == 2:
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x, 2))
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x + self.size * 8, 2))
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x + self.size * 13, 2))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x, 2))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x - self.size * 8, 2))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x, 2))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x + self.size * 7, 2))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x + self.size * 12, 2))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x, 2))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x  - self.size * 5, 2))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x  - self.size * 13, 2))
            group.add(Vehicle('racecar2', self.screen_width, self.screen_height, self.size, racecar_x, 2))
            group.add(Vehicle('racecar2', self.screen_width, self.screen_height, self.size, racecar_x + self.size * 5, 2))
        elif level >= 3:
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x, 3))
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x + self.size * 5, 3))
            group.add(Vehicle('car', self.screen_width, self.screen_height, self.size, car_x + self.size * 10, 3))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x, 3))
            group.add(Vehicle('racecar', self.screen_width, self.screen_height, self.size, racecar_x - self.size * 4, 3))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x, 3))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x + self.size * 6, 3))
            group.add(Vehicle('truck', self.screen_width, self.screen_height, self.size, truck_x + self.size * 10, 3))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x, 3))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x  - self.size * 5, 3))
            group.add(Vehicle('car2', self.screen_width, self.screen_height, self.size, car_x  - self.size * 10, 3))
            group.add(Vehicle('racecar2', self.screen_width, self.screen_height, self.size, racecar_x, 3))
            group.add(Vehicle('racecar2', self.screen_width, self.screen_height, self.size, racecar_x + self.size * 5, 3))

    def spawn_lilies(self, group, level):
        y = self.size + self.size / 4 + 2
        x = 19
        bonus_active = False
        croc_active = False
        if level == 1:
            for i in range(5):
                x = 19 + i * self.size * 3
                random_nbr = randint(1, 14)
                if random_nbr < 4 and not bonus_active:
                    print("Bonus lily")
                    bonus_active = True
                    group.add(BonusLily(x, y))
                else:
                    print("Ordinary lily")
                    group.add(OrdinaryLily(x, y))
        if level == 2:
            for i in range(5):
                x = 19 + i * self.size * 3
                random_nbr = randint(1, 14)
                if random_nbr < 5 and not bonus_active and not croc_active:
                    print("Bonus lily")
                    bonus_active = True
                    group.add(BonusLily(x, y))
                elif random_nbr < 11 and not bonus_active and not croc_active:
                    print("Croc lily")
                    croc_active = True
                    group.add(CrocodileLily(x, y))
                else:
                    print("Ordinary lily")
                    group.add(OrdinaryLily(x, y))
        if level >= 3:
            for i in range(5):
                x = 19 + i * self.size * 3
                random_nbr = randint(1, 14)
                if random_nbr < 3 and not bonus_active and not croc_active:
                    print("Bonus lily")
                    bonus_active = True
                    group.add(BonusLily(x, y))
                elif random_nbr < 11 and not bonus_active and not croc_active:
                    print("Croc lily")
                    croc_active = True
                    group.add(CrocodileLily(x, y))
                else:
                    print("Ordinary lily")
                    group.add(OrdinaryLily(x, y))