import pygame

class Frog: 
    def __init__(self):
        from main import SCREENWIDTH, SCREENHEIGHT, SIZE
        self.image = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = SCREENWIDTH / 2 
        self.rect.y = SCREENHEIGHT - SIZE 
        self.velocity = 5
        self.velX,self.velY = 0, 0
