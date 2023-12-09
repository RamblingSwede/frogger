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

            self.frog.rect.x += self.frog.velX
            self.frog.rect.y += self.frog.velY
            pygame.display.update()
            self.clock.tick(FPS)

Game().run()