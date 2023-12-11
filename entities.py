import pygame

class Frog: 
    def __init__(self, width, height, size):
        self.image = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = width / 2 
        self.rect.y = height - size 
        self.velocity = 5
        self.velX,self.velY = 0, 0
