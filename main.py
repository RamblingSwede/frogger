from entities import *
from utils import *
from random import randint 
import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 14, SIZE * 15
FPS = 60
LEFT_DIR    = [pygame.K_a, pygame.K_LEFT]
RIGHT_DIR   = [pygame.K_d, pygame.K_RIGHT] 
UP_DIR      = [pygame.K_w, pygame.K_UP] 
DOWN_DIR    = [pygame.K_w, pygame.K_DOWN] 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger - Level 1')
        self.level              = 1
        self.clock              = pygame.time.Clock()
        self.screen             = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
        self.background         = Background(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.ui                 = UI(SCREENHEIGHT - SIZE)
        self.running            = True
        self.safe_frogs         = 0
        self.lives_left         = 2
        self.floater_group      = pygame.sprite.Group() 
        self.vehicle_group      = pygame.sprite.Group()
        self.final_lilies_group = pygame.sprite.Group() 
        self.frog               = pygame.sprite.GroupSingle()
        self.frog.add(Frog(SCREENWIDTH, SCREENHEIGHT, SIZE)) 
        self.timer              = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 30000)
        self.movementX          = [False, False]
        self.movementY          = [False, False]
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.spawn_floaters()
        self.spawn_vehicles() 
        self.spawn_final_lilies() 

    def spawn_floaters(self): 
        log_small_x = randint(-SIZE * 4, -SIZE * 2)
        log_medium_x = randint(-SIZE * 10, -SIZE * 4)
        log_large_x = randint(-SIZE * 8, -SIZE * 3)
        lily_medium_x = randint(SIZE * 9, SCREENWIDTH + SIZE * 4)
        lily_large_x = randint(SIZE * 6, SCREENWIDTH + SIZE * 2)
        self.floater_group.add(Floater('log_small', SCREENWIDTH, SIZE, log_small_x))
        self.floater_group.add(Floater('log_small', SCREENWIDTH, SIZE, log_small_x - SCREENWIDTH / 3 - SIZE))
        self.floater_group.add(Floater('log_small', SCREENWIDTH, SIZE, log_small_x - 2 * SCREENWIDTH / 3 - SIZE))
        self.floater_group.add(Floater('log_medium', SCREENWIDTH, SIZE, log_medium_x))
        self.floater_group.add(Floater('log_medium', SCREENWIDTH, SIZE, log_medium_x - SIZE * 6))
        self.floater_group.add(Floater('log_medium', SCREENWIDTH, SIZE, log_medium_x - SIZE * 11))
        self.floater_group.add(Floater('log_medium', SCREENWIDTH, SIZE, log_medium_x - SIZE * 16))
        self.floater_group.add(Floater('log_large', SCREENWIDTH, SIZE, log_large_x))
        self.floater_group.add(Floater('log_large', SCREENWIDTH, SIZE, log_large_x - SIZE * 8))
        self.floater_group.add(Floater('log_large', SCREENWIDTH, SIZE, log_large_x - SIZE * 16))
        self.floater_group.add(Floater('lily_medium', SCREENWIDTH, SIZE, lily_medium_x))
        self.floater_group.add(Floater('lily_medium', SCREENWIDTH, SIZE, lily_medium_x + SIZE * 5))
        self.floater_group.add(Floater('lily_medium', SCREENWIDTH, SIZE, lily_medium_x + SIZE * 10))
        self.floater_group.add(Floater('lily_medium', SCREENWIDTH, SIZE, lily_medium_x + SIZE * 15))
        self.floater_group.add(Floater('lily_large', SCREENWIDTH, SIZE, lily_large_x))
        self.floater_group.add(Floater('lily_large', SCREENWIDTH, SIZE, lily_large_x + SIZE * 5))
        self.floater_group.add(Floater('lily_large', SCREENWIDTH, SIZE, lily_large_x + SIZE * 10))
        self.floater_group.add(Floater('lily_large', SCREENWIDTH, SIZE, lily_large_x + SIZE * 15))

    def spawn_vehicles(self): 
        car_x = randint(SIZE * 2, SIZE * 8)
        tractor_x = randint(SIZE * 2, SIZE * 8)
        truck_x = randint(SIZE * 6, SIZE * 10)
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x))
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 5))
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 10))
        self.vehicle_group.add(Vehicle('tractor', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x))
        self.vehicle_group.add(Vehicle('tractor', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x - SIZE * 4))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x + SIZE * 6))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x + SIZE * 10))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x  - SIZE * 5))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x  - SIZE * 10))
        self.vehicle_group.add(Vehicle('tractor2', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x))
        self.vehicle_group.add(Vehicle('tractor2', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 4))

    def spawn_final_lilies(self): 
        y = SIZE + SIZE / 4 + 2 
        for i in range(5): 
            x = 16 + 6 + i * SIZE * 3 
            self.final_lilies_group.add(Final_Lily(x, y))

    def collision(self):
        self.handle_vehicle_hit() 
        self.handle_floater_hit() 
        self.handle_final_platform_hit() 

    def handle_vehicle_hit(self): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.vehicle_group, False):
            self.lose_life() 

    def handle_floater_hit(self): 
        if self.in_river():
            if pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False):
                platforms = pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False)
                for platform in platforms:
                    if platform.within_bounds(self.frog.sprite.rect.x, SIZE): 
                        self.frog.sprite.match_speed(platform.offset, platform.velocity)
                    else:
                        self.lose_life() 
            else:
                self.lose_life() 

    def handle_final_platform_hit(self): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.final_lilies_group, False): 
            lily = pygame.sprite.spritecollide(self.frog.sprite, self.final_lilies_group, False)[0] 
            if lily.hit(self.frog.sprite.get_x(), SIZE): 
                lily.set_occupied() 
                if self.safe_frogs == 4:
                    self.level_completed()
                else:
                    self.safe_frogs += 1
                    print('Frog made it to safety')
                    self.respawn()
            else: 
                print('Didnt hit')
                self.lose_life() 
        elif self.frog.sprite.rect.y == SIZE:
            self.lose_life() 

    def in_river(self): 
        return self.frog.sprite.rect.y < SIZE * 7 and self.frog.sprite.rect.y > SIZE

    def lose_life(self): 
        if self.lives_left > 0:
            self.lives_left -= 1
            self.respawn()
        else:
            self.game_over()

    def respawn(self):
        pygame.time.set_timer(self.timer, 30000)
        self.ui.update(str(self.lives_left))
        self.frog.sprite.rect.x = SCREENWIDTH / 2
        self.frog.sprite.rect.y = SCREENHEIGHT - SIZE * 2
            
    def game_over(self):
        print('Press Space to restart')
        self.running = False

    def level_completed(self):
        print('Level completed')
        self.level += 1
        pygame.display.set_caption('Frogger - Level ' + str(self.level))
        self.respawn()
                    
    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.update(SCREENWIDTH, SCREENHEIGHT, SIZE, self.vehicle_group)
        self.vehicle_group.draw(self.screen)
        self.floater_group.update(SCREENWIDTH, SIZE, self.floater_group)
        self.floater_group.draw(self.screen)
        self.final_lilies_group.draw(self.screen) 
        self.frog.update(SCREENWIDTH, SCREENHEIGHT, SIZE, (self.movementX[0], self.movementX[1]), (self.movementY[0], self.movementY[1]))
        self.frog.draw(self.screen)
        self.ui.draw(self.screen)

    def run(self):
        while True:
            self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
            #print('Remaining time: ' + str(30 - self.current_time))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()        
                if event.type == pygame.KEYDOWN:
                    if event.key in LEFT_DIR:
                        self.movementX[0] = True
                    if event.key in RIGHT_DIR:
                        self.movementX[1] = True
                    if event.key in UP_DIR:
                        self.movementY[1] = True
                    if event.key in DOWN_DIR:
                        self.movementY[0] = True
                    if event.key == pygame.K_SPACE:
                        ##Only exists for debug, to be replaced with restart menu at some point
                        self.running = True
                        self.start_time = int(pygame.time.get_ticks() / 1000)
                        #self.level_completed()
                        self.safe_frogs = 0
                        self.lives_left = 2
                        self.respawn()
                if event.type == pygame.KEYUP:
                    if event.key in LEFT_DIR:
                        self.movementX[0] = False
                    if event.key in RIGHT_DIR:
                        self.movementX[1] = False
                    if event.key in UP_DIR:
                        self.movementY[1] = False
                    if event.key in DOWN_DIR:
                        self.movementY[0] = False
                if event.type == self.timer:
                    if self.lives_left > 0:
                        print('Ran out of time')
                        self.lives_left -= 1
                        self.respawn()
                    else:
                        print('Ran out of time')
                        self.game_over()
            if self.running:
                self.collision()
                self.update_display() 
                pygame.display.update()
                self.clock.tick(FPS)

Game().run()