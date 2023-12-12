import pygame

class Frog: 
    def __init__(self, width, height, size):
        self.image          = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect           = self.image.get_rect()
        self.rect.x         = width / 2 
        self.rect.y         = height - size 
        self.velocity       = 5
        self.velX,self.velY = 0, 0

    def update_position(self): 
        self.rect.x += self.velX
        self.rect.y += self.velY

    def draw(self, screen): 
        screen.blit(self.image, self.rect)

class Background: 
    RIVER_SIZE = 5 

    def __init__(self, width, height, size): 
        self.safe_platform_image    = pygame.image.load("./resources/safe_platform_placeholder.png").convert_alpha() 
        self.river_image            = pygame.image.load("./resources/river_placeholder.png").convert_alpha() 
        self.finish_platform_image  = pygame.image.load("./resources/finish_platform_placeholder.png").convert_alpha() 
        self.width = width 
        self.height = height
        self.size = size 

    def draw(self, screen): 
        self.draw_safe_platforms(screen) 
        self.draw_river(screen) 
        self.draw_finish_platform(screen) 

    def draw_safe_platforms(self, screen): 
        self.safe_platform      = self.safe_platform_image.get_rect() 
        self.safe_platform.y    = self.height - self.size 
        screen.blit(self.safe_platform_image, self.safe_platform)
        self.safe_platform.y    = self.RIVER_SIZE * self.size + self.size 
        screen.blit(self.safe_platform_image, self.safe_platform)
    
    def draw_river(self, screen): 
        self.river = self.river_image.get_rect() 
        for i in range(self.RIVER_SIZE): 
            self.river.y = (i + 1) * self.size 
            screen.blit(self.river_image, self.river) 

    def draw_finish_platform(self, screen): 
        self.finish_platform = self.finish_platform_image.get_rect() 
        screen.blit(self.finish_platform_image, self.finish_platform)

class Floater: 
    def __init__(self, x, height, width, delay, velocity, offset, image): 
        self.velocity = velocity
        self.image = image 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = height
        self.width = width 
        self.offset = offset 
        self.delay = delay 
        self.count = 0 
    
    def update_location(self): 
        if self.count == self.offset: 
            if self.rect.x >= self.width: 
                self.rect.x = 0 - self.delay 
            else: 
                self.rect.x += self.velocity 
            self.count = 0 
        self.count += 1 

    def draw(self, screen): 
        screen.blit(self.image, self.rect) 