import pygame

class Frog(pygame.sprite.Sprite): 
    def __init__(self, width, height, size):
        super().__init__()
        self.image          = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect           = self.image.get_rect()
        self.rect.x         = width / 2 
        self.rect.y         = height - size * 2
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
        if self.rect.y >= height - size * 2:
                self.rect.y = height - size * 2
        if self.rect.y <= 0:
                self.rect.y = 0
    
    def get_x(self): 
        return self.rect.x 

class Final_Lily(pygame.sprite.Sprite): 
    WIDTH = 20 

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load("./resources/final_lily_placeholder.png").convert_alpha() 
        self.rect           = self.image.get_rect()
        self.rect.x         = x 
        self.rect.y         = y 
        self.occupied       = False 

    def hit(self, x_left, size): 
        if self.occupied: 
            return False 
        x_right = x_left + size 
        mid = self.rect.x + self.WIDTH / 2
        return x_left < mid and x_right > mid 

    def set_safe(self): 
        x           = self.rect.x 
        self.image  = pygame.image.load("./resources/frog_placeholder.png").convert_alpha() 
        self.rect   = self.image.get_rect()
        self.rect.x = x - 6 
        self.rect.y = 32 

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

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
            self.rect.y = size * 5 
            self.velocity = 1
            self.offset = 3
            self.delay = -self.width
        if self.type == 'log_medium':
            self.image = pygame.image.load("./resources/log_3_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = 3 * size 
            self.rect.x = start_x
            self.rect.y = size * 2
            self.velocity = 1
            self.offset = 2 
            self.delay = -(self.width * 3 + size)
        if self.type == 'log_large':
            self.image = pygame.image.load("./resources/log_4_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 4 * size 
            self.rect.x = start_x
            self.rect.y = size * 4
            self.velocity = 1
            self.offset = 1
            self.delay = -(self.width + size) * 2
        if self.type == 'lily_medium':
            self.image = pygame.image.load("./resources/lily_2_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 2 * size 
            self.rect.x = start_x
            self.rect.y = size * 3
            self.velocity = -1
            self.offset = 1 
            self.delay = width + self.width * 2
        if self.type == 'lily_large':
            self.image = pygame.image.load("./resources/lily_3_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = 3 * size 
            self.rect.x = start_x
            self.rect.y = size * 6
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
        
    def within_bounds(self, x_left, size): 
        x_right = x_left + size 
        margin = size * (4 / 10)
        return x_left > self.rect.x - margin and x_right < self.rect.x + self.width + margin 

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
            self.rect.y = height - size * 3
            self.velocity = -1
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'car2':
            self.image = pygame.image.load("./resources/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 6
            self.velocity = 1
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor':
            self.image = pygame.image.load("./resources/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 4
            self.velocity = 2 
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor2':
            self.image = pygame.image.load("./resources/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 7
            self.velocity = -2 
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'truck':
            self.image = pygame.image.load("./resources/truck_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size * 2
            self.rect.x = start_x
            self.rect.y = height - size * 5
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