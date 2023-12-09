from entities import Frog
import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 40, 720
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))   
        self.frog = Frog()
        self.velx,self.vely = 0, 0
        
    def run(self):
        while True:
            self.screen.fill('Black')
            self.screen.blit(self.frog.image, self.frog.rect)
            
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                            self.velx -= 5
                    if event.key == pygame.K_d:
                            self.velx += 5
                    if event.key == pygame.K_w:
                            self.vely -= 5
                    if event.key == pygame.K_s:                    
                            self.vely += 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                            self.velx = 0
                    if event.key == pygame.K_d:
                            self.velx = 0
                    if event.key == pygame.K_w:
                            self.vely = 0
                    if event.key == pygame.K_s:
                            self.vely = 0

            self.frog.rect.x += self.velx
            self.frog.rect.y += self.vely
            pygame.display.update()
            self.clock.tick(FPS)

Game().run()