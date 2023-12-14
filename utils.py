import pygame

class UI:
    def __init__(self, height):
        self.image = pygame.image.load("./resources/bottom_UI_two_lives.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = height

    def update(self, type):
        if type == '2':
            self.image = pygame.image.load("./resources/bottom_UI_two_lives.png").convert_alpha()
        if type == '1':
            self.image = pygame.image.load("./resources/bottom_UI_one_life.png").convert_alpha()
        if type == '0':
            self.image = self.image = pygame.image.load("./resources/bottom_UI_no_lives.png").convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect)