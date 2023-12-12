from entities import *
from entity_list import * 
from random import randint, choice
import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 14, SIZE * 11 
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger')
        self.clock      = pygame.time.Clock()
        self.screen     = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
        self.background = Background(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.floaters   = self.add_river_floaters()
        self.vehicle_group = pygame.sprite.Group()
        self.frog = pygame.sprite.GroupSingle()
        self.frog.add(Frog(SCREENWIDTH, SCREENHEIGHT, SIZE)) 
        self.vehicle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.vehicle_timer,2000)
        self.movementX = [False, False]
        self.movementY = [False, False]

    def add_river_floaters(self): 
        log_2 = Floater(0, 128, SCREENWIDTH, SIZE * 2, 1, 3, pygame.image.load("./resources/log_2_placeholder.png").convert_alpha())
        log_3 = Floater(0, 32, SCREENWIDTH, SIZE * 3, 1, 2, pygame.image.load("./resources/log_3_placeholder.png").convert_alpha())
        log_4 = Floater(0, 96, SCREENWIDTH, SIZE * 4, 1, 1, pygame.image.load("./resources/log_4_placeholder.png").convert_alpha())
        lily_2 = Floater(0, 64, SCREENWIDTH, SIZE * 2, 1, 1, pygame.image.load("./resources/lily_2_placeholder.png").convert_alpha())
        lily_3 = Floater(0, 160, SCREENWIDTH, SIZE * 3, 1, 2, pygame.image.load("./resources/lily_3_placeholder.png").convert_alpha())
        return entity_list([log_2, log_3, log_4, lily_2, lily_3])

    def collision(self):
        if pygame.sprite.spritecollide(self.frog.sprite,self.vehicle_group, False):
            print('Collision')

    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.draw(self.screen)
        self.vehicle_group.update(SCREENWIDTH, SIZE)
        self.floaters.update_locations() 
        self.floaters.draw(self.screen) 
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
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movementX[0] = False
                    if event.key == pygame.K_d:
                        self.movementX[1] = False
                    if event.key == pygame.K_w:
                        self.movementY[1] = False
                    if event.key == pygame.K_s:
                        self.movementY[0] = False
                if event.type == self.vehicle_timer:
                    self.vehicle_group.add(Vehicle(choice(['car','truck', 'tractor']), SCREENWIDTH, SCREENHEIGHT, SIZE))
            self.collision()
            self.update_display() 
            pygame.display.update()
            self.clock.tick(FPS)

Game().run()