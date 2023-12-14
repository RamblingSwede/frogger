import pygame

class Frog(pygame.sprite.Sprite): 
    def __init__(self, width, height, size):
        super().__init__()
        self.image          = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect           = self.image.get_rect()
        self.rect.x         = width / 2 
        self.rect.y         = height - size
        self.hop_cooldown   = 20
        self.hop_cooldownX  = self.hop_cooldown
        self.hop_cooldownY  = self.hop_cooldown
        self.count          = 0

    def update(self, width, height, size, movementX = (0,0), movementY = (0,0)): 
        self.out_of_bounds(width, height, size)
        if movementX[0] == True and movementY[0] == False and movementY[1] == False:
            if self.hop_cooldownX == self.hop_cooldown:
                self.hop_cooldownX = 0
                self.rect.x -= size
            self.hop_cooldownX += 1
        elif movementX[1] == True and movementY[0] == False and movementY[1] == False:
            if self.hop_cooldownX == self.hop_cooldown:
                self.hop_cooldownX = 0
                self.rect.x += size
            self.hop_cooldownX += 1
        else:
            self.velX = 0
            self.hop_cooldownX = self.hop_cooldown
        if movementY[1] == True and movementX[0] == False and movementX[1] == False:
            if self.hop_cooldownY == self.hop_cooldown:
                self.hop_cooldownY = 0
                self.rect.y -= size
            self.hop_cooldownY += 1
        elif movementY[0] == True and movementX[0] == False and movementX[1] == False:
            if self.hop_cooldownY == self.hop_cooldown:
                self.hop_cooldownY = 0
                self.rect.y += size
            self.hop_cooldownY += 1
        else:
            self.velY = 0
            self.hop_cooldownY = self.hop_cooldown
        
    def match_speed(self, offset, velocity):
        if self.count == offset: 
            self.rect.x += velocity
            self.count = 0 
        if self.count >= 3:
            self.count = 0
        self.count += 1 

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
    def __init__(self, type, width, size, start_x):
        super().__init__()
        self.type = type 
        self.count = 0 
        if self.type == 'log_small':
            self.image = pygame.image.load("./resources/log_2_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 2 * size 
            self.rect.x = start_x
            self.rect.y = size * 4 
            self.velocity = 1
            self.offset = 3
            self.delay = -self.width
        if self.type == 'log_medium':
            self.image = pygame.image.load("./resources/log_3_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = 3 * size 
            self.rect.x = start_x
            self.rect.y = size 
            self.velocity = 1
            self.offset = 2 
            self.delay = -(self.width * 3 + size)
        if self.type == 'log_large':
            self.image = pygame.image.load("./resources/log_4_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 4 * size 
            self.rect.x = start_x
            self.rect.y = size * 3 
            self.velocity = 1
            self.offset = 1
            self.delay = -(self.width + size) * 2
        if self.type == 'lily_medium':
            self.image = pygame.image.load("./resources/lily_2_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 2 * size 
            self.rect.x = start_x
            self.rect.y = size * 2
            self.velocity = -1
            self.offset = 1 
            self.delay = width + self.width * 2
        if self.type == 'lily_large':
            self.image = pygame.image.load("./resources/lily_3_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 3 * size 
            self.rect.x = start_x
            self.rect.y = size * 5
            self.velocity = -1
            self.offset = 2 
            self.delay = width + self.width 

    def update(self, width, size, group):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.count = 0 
            if self.destroy(width, size): 
                group.add(Floater(self.type, width, size, self.delay))
        self.count += 1 

    def destroy(self, width, size):
        if self.velocity > 0: 
            if self.rect.x >= width: 
                self.kill()
                return True 
            return False
        else: 
            if self.rect.x <= -self.width: 
                self.kill() 
                return True
            return False 

class Vehicle(pygame.sprite.Sprite): 
    def __init__(self, type, width, height, size, start_x):
        super().__init__()
        self.type = type 
        self.count = 0 
        if type == 'car':
            self.image = pygame.image.load("./resources/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 2
            self.velocity = -1
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'car2':
            self.image = pygame.image.load("./resources/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 5
            self.velocity = 1
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor':
            self.image = pygame.image.load("./resources/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 3
            self.velocity = 2 
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor2':
            self.image = pygame.image.load("./resources/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 6
            self.velocity = -2 
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'truck':
            self.image = pygame.image.load("./resources/truck_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size * 2
            self.rect.x = start_x
            self.rect.y = height - size * 4
            self.velocity = -1
            self.offset = 2 
            self.delay = width + self.width * 2

    def update(self, width, height, size, group):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.count = 0 
            if self.destroy(width, size): 
                group.add(Vehicle(self.type, width, height, size, self.delay))
        self.count += 1 

    def destroy(self, width, size):
        if self.velocity > 0: 
            if self.rect.x >= width: 
                self.kill()
                return True 
            return False
        else: 
            if self.rect.x <= -self.width: 
                self.kill() 
                return True
            return False 