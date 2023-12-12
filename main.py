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
        self.clock          = pygame.time.Clock()
        self.screen         = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
        self.background     = Background(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.floater_group  = pygame.sprite.Group() 
        self.vehicle_group  = pygame.sprite.Group()
        self.frog           = pygame.sprite.GroupSingle()
        self.frog.add(Frog(SCREENWIDTH, SCREENHEIGHT, SIZE)) 
        self.timer          = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer, 2000)
        self.movementX      = [False, False]
        self.movementY      = [False, False]

    def collision(self):
        if pygame.sprite.spritecollide(self.frog.sprite,self.vehicle_group, False):
            print('Collision')
        elif pygame.sprite.spritecollide(self.frog.sprite,self.floater_group, False):
            print('Collision')

    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.draw(self.screen)
        self.vehicle_group.update(SCREENWIDTH, SIZE)
        self.floater_group.draw(self.screen)
        self.floater_group.update(SCREENWIDTH, SIZE)
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
                if event.type == self.timer:
                    self.vehicle_group.add(Vehicle(choice(['car','truck', 'tractor']), SCREENWIDTH, SCREENHEIGHT, SIZE))
                    self.floater_group.add(Floater1(choice(['log_small','log_medium', 'log_large', 'lily_medium', 'lily_large']), SCREENWIDTH, SIZE))
            self.collision()
            self.update_display() 
            pygame.display.update()
            self.clock.tick(FPS)

Game().run()