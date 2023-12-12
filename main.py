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
        self.frog       = Frog(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.floaters   = self.add_river_floaters()
        self.vehicle_group = pygame.sprite.Group()
        self.vehicle_rect_list = []
        self.update_display() 
        self.vehicle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.vehicle_timer,1500)

    def add_river_floaters(self): 
        log_2 = Floater(0, 128, SCREENWIDTH, SIZE * 2, 1, 3, pygame.image.load("./resources/log_2_placeholder.png").convert_alpha())
        log_3 = Floater(0, 32, SCREENWIDTH, SIZE * 3, 1, 2, pygame.image.load("./resources/log_3_placeholder.png").convert_alpha())
        log_4 = Floater(0, 96, SCREENWIDTH, SIZE * 4, 1, 1, pygame.image.load("./resources/log_4_placeholder.png").convert_alpha())
        lily_2 = Floater(0, 64, SCREENWIDTH, SIZE * 2, 1, 1, pygame.image.load("./resources/lily_2_placeholder.png").convert_alpha())
        lily_3 = Floater(0, 160, SCREENWIDTH, SIZE * 3, 1, 2, pygame.image.load("./resources/lily_3_placeholder.png").convert_alpha())
        return entity_list([log_2, log_3, log_4, lily_2, lily_3])

    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.draw(self.screen)
        self.vehicle_group.update()
        self.floaters.update_locations() 
        self.floaters.draw(self.screen) 
        self.frog.update_position() 
        self.frog.draw(self.screen) 

    def run(self):
        while True:
            if self.frog.rect.x >= SCREENWIDTH - SIZE:
                  self.frog.rect.x = SCREENWIDTH - SIZE
            if self.frog.rect.x <= 0:
                  self.frog.rect.x = 0
            if self.frog.rect.y >= SCREENHEIGHT - SIZE:
                  self.frog.rect.y = SCREENHEIGHT - SIZE
            if self.frog.rect.y <= 0:
                  self.frog.rect.y = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == self.vehicle_timer:
                    self.vehicle_group.add(Vehicle(choice(['car','truck', 'tractor']), SCREENWIDTH, SCREENHEIGHT, SIZE))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a and self.frog.velY == 0:
                            self.frog.velX -= self.frog.velocity
                    if event.key == pygame.K_d and self.frog.velY == 0:
                            self.frog.velX += self.frog.velocity
                    if event.key == pygame.K_w and self.frog.velX == 0:
                            self.frog.velY -= self.frog.velocity
                    if event.key == pygame.K_s and self.frog.velX == 0:                    
                            self.frog.velY += self.frog.velocity
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                            self.frog.velX = 0
                    if event.key == pygame.K_d:
                            self.frog.velX = 0
                    if event.key == pygame.K_w:
                            self.frog.velY = 0
                    if event.key == pygame.K_s:
                            self.frog.velY = 0

            self.update_display() 
            pygame.display.update()
            self.clock.tick(FPS)

Game().run()