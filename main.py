from entities import *
from entity_list import * 
from random import randint, choice
import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 14, SIZE * 13
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger')
        self.clock          = pygame.time.Clock()
        self.screen         = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
        self.background     = Background(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.running        = True
        self.safe_frogs     = 0
        self.lives_left     = 2
        self.floater_group  = pygame.sprite.Group() 
        self.vehicle_group  = pygame.sprite.Group()
        self.frog           = pygame.sprite.GroupSingle()
        self.frog.add(Frog(SCREENWIDTH, SCREENHEIGHT, SIZE)) 
        self.timer          = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 30000)
        self.movementX      = [False, False]
        self.movementY      = [False, False]
        self.spawn_floaters()
        self.spawn_vehicles() 

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

    def collision(self):
        if pygame.sprite.spritecollide(self.frog.sprite, self.vehicle_group, False):
            if self.lives_left > 0:
                self.lives_left -= 1
                self.respawn()
            else:
                self.game_over()
        if self.frog.sprite.rect.y < 190 and self.frog.sprite.rect.y > 0:
            if pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False):
                platforms = pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False)
                for platform in platforms:
                    if self.frog.sprite.rect.x + SIZE in range(platform.rect.x + SIZE, platform.rect.x + platform.width):
                        self.frog.sprite.match_speed(platform.offset, platform.velocity)
                    else:
                        if self.lives_left > 0:
                            self.lives_left -= 1
                            self.respawn()
                        else:
                            self.game_over()
            else:
                if self.lives_left > 0:
                    self.lives_left -= 1
                    self.respawn()
                else:
                    self.game_over()
        if self.frog.sprite.rect.y == 0:
            if self.safe_frogs == 4:
                self.level_completed()
            else:
                self.safe_frogs += 1
                self.respawn()

    def respawn(self):
        pygame.time.set_timer(self.timer, 30000)
        self.frog.sprite.rect.x = SCREENWIDTH / 2
        self.frog.sprite.rect.y = SCREENHEIGHT - SIZE
            
    def game_over(self):
        print('Out of lives')
        print('Press Space to restart')
        self.running = False

    def level_completed(self):
        print('Level completed')
        print('Press Space to restart')
        self.running = False
                    
    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.update(SCREENWIDTH, SCREENHEIGHT, SIZE, self.vehicle_group)
        self.vehicle_group.draw(self.screen)
        self.floater_group.update(SCREENWIDTH, SIZE, self.floater_group)
        self.floater_group.draw(self.screen)
        self.frog.update(SCREENWIDTH, SCREENHEIGHT, SIZE, (self.movementX[0], self.movementX[1]), (self.movementY[0], self.movementY[1]))
        self.frog.draw(self.screen)  

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movementX[0] = True
                    if event.key == pygame.K_d:
                        self.movementX[1] = True
                    if event.key == pygame.K_w:
                        self.movementY[1] = True
                    if event.key == pygame.K_s:
                        self.movementY[0] = True
                    if event.key == pygame.K_SPACE:
                        ##Only exists for debug, to be replaced with restart menu at some point
                        self.running = True
                        self.safe_frogs = 0
                        self.lives_left = 2
                        self.respawn()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movementX[0] = False
                    if event.key == pygame.K_d:
                        self.movementX[1] = False
                    if event.key == pygame.K_w:
                        self.movementY[1] = False
                    if event.key == pygame.K_s:
                        self.movementY[0] = False
                if event.type == self.timer:
                    if self.lives_left > 0:
                        print('Ran out of time')
                        self.lives_left -= 1
                        self.respawn()
                    else:
                        print('Ran out of time')
                        self.game_over()
                    #print('Spawning vehicle') 
                    #self.vehicle_group.add(Vehicle(choice(['car','truck', 'tractor']), SCREENWIDTH, SCREENHEIGHT, SIZE))
                    #self.floater_group.add(Floater(choice(['log_small','log_medium', 'log_large', 'lily_medium', 'lily_large']), SCREENWIDTH, SIZE))
            if self.running:
                self.collision()
                self.update_display() 
                pygame.display.update()
                self.clock.tick(FPS)

Game().run()