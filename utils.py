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

class Background: 
    RIVER_SIZE = 5

    def __init__(self, width, height, size): 
        self.safe_platform_image    = pygame.image.load("./resources/safe_platform_placeholder.png").convert_alpha() 
        self.river_image            = pygame.image.load("./resources/river_placeholder.png").convert_alpha() 
        self.finish_platform_image  = pygame.image.load("./resources/finish_platform_placeholder_new.png").convert_alpha() 
        self.width  = width 
        self.height = height
        self.size   = size 

    def draw(self, screen): 
        self.draw_safe_platforms(screen) 
        self.draw_river(screen) 
        self.draw_finish_platform(screen) 

    def draw_safe_platforms(self, screen): 
        self.safe_platform      = self.safe_platform_image.get_rect() 
        self.safe_platform.y    = self.height - self.size * 2
        screen.blit(self.safe_platform_image, self.safe_platform)
        self.safe_platform.y    = self.RIVER_SIZE * self.size + self.size + self.size
        screen.blit(self.safe_platform_image, self.safe_platform)
    
    def draw_river(self, screen): 
        river = self.river_image.get_rect() 
        for i in range(self.RIVER_SIZE + 1): 
            river.y = (i + 1) * self.size 
            screen.blit(self.river_image, river) 

    def draw_finish_platform(self, screen): 
        finish_platform = self.finish_platform_image.get_rect() 
        finish_platform.y  = 0 + self.size
        screen.blit(self.finish_platform_image, finish_platform)