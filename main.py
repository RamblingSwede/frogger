import pygame
import sys


SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 60

class Frog: 
    def __init__(self):
        self.image = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.frog.rect.x -= 32
                    if event.key == pygame.K_d:
                        self.frog.rect.x += 32
                    if event.key == pygame.K_w:
                        self.frog.rect.y -= 32
                    if event.key == pygame.K_s:
                        self.frog.rect.y += 32

            pygame.display.update()
            self.clock.tick(60)

Game().run()