import pygame

class Frog(pygame.sprite.Sprite): 
    def __init__(self, width, height, size):
        super().__init__()
        self.image          = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect           = self.image.get_rect()
        self.rect.x         = width / 2 
        self.rect.y         = height - size 
        self.velocity       = 2
        self.velX,self.velY = 0, 0

    def update(self, width, height, size, movementX = (0,0), movementY = (0,0)): 
        self.out_of_bounds(width, height, size)
        if movementX[0] and self.velY == 0:
            self.velX = - self.velocity
        elif movementX[1] and self.velY == 0:
            self.velX = + self.velocity
        else:
            self.velX = 0
        if movementY[1] and self.velX == 0:
            self.velY = - self.velocity
        elif movementY[0] and self.velX == 0:
            self.velY = + self.velocity
        else:
            self.velY = 0
        self.rect.x += self.velX
        self.rect.y += self.velY

    def out_of_bounds(self, width, height, size):
        if self.rect.x >= width - size:
            self.rect.x = width - size
        if self.rect.x <= 0:
                self.rect.x = 0
        if self.rect.y >= height - size:
                self.rect.y = height - size
        if self.rect.y <= 0:
                self.rect.y = 0

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

class Floater(pygame.sprite.Sprite): 
    def __init__(self, type, width, size):
        super().__init__()
        from random import randint
        self.count = 0 
        if type == 'log_small':
            self.image = pygame.image.load("./resources/log_2_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = -randint(size, size * 2)
            self.rect.y = size * 4 
            self.velocity = 1
            self.offset = 3
        if type == 'log_medium':
            self.image = pygame.image.load("./resources/log_3_placeholder.png")
            self.rect  = self.image.get_rect()
            self.rect.x = -randint(size * 2, size * 4)
            self.rect.y = size 
            self.velocity = 1
            self.offset = 2
        if type == 'log_large':
            self.image = pygame.image.load("./resources/log_4_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = -randint(size * 3, size * 6)
            self.rect.y = size * 3 
            self.velocity = 1
            self.offset = 1
        if type == 'lily_medium':
            self.image = pygame.image.load("./resources/lily_2_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = width + randint(0, size * 2)
            self.rect.y = size * 2
            self.velocity = -1
            self.offset = 1
        if type == 'lily_large':
            self.image = pygame.image.load("./resources/lily_3_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = width + randint(0, size * 3)
            self.rect.y = size * 5
            self.velocity = -1
            self.offset = 2 
        

    def update(self, width, size):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.destroy(width, size)
            self.count = 0 
        self.count += 1 

    def destroy(self, width, size):
        if self.rect.x <= -130 or self.rect.x >= width + size * 8:
            self.kill()

class Vehicle(pygame.sprite.Sprite): 
    def __init__(self, type, width, height, size):
        super().__init__()
        from random import randint
        self.count = 0 
        if type == 'car':
            self.image = pygame.image.load("./resources/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = width + randint(size, size * 4)
            self.rect.y = height - size * 2
            self.velocity = -1
            self.offset = 1 
        if type == 'tractor':
            self.image = pygame.image.load("./resources/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.rect.x = -randint(size, size * 4)
            self.rect.y = height - size * 3
            self.velocity = 2 
            self.offset = 1 
        if type == 'truck':
            self.image = pygame.image.load("./resources/truck_placeholder.png")
            self.rect = self.image.get_rect()
            self.rect.x = width + randint(size * 2, size * 8)
            self.rect.y = height - size * 4
            self.velocity = -1
            self.offset = 2 
        

    def update(self, width, size):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.destroy(width, size)
            self.count = 0 
        self.count += 1 

    def destroy(self, width, size):
        if self.rect.x <= -130 or self.rect.x >= width + size * 8:
            self.kill()