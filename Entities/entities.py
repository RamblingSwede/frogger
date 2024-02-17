import pygame

class Frog(pygame.sprite.Sprite): 
    def __init__(self, width, height, size):
        super().__init__()
        self.image          = pygame.image.load("./resources/misc/frog_placeholder.png").convert_alpha()
        self.rect           = self.image.get_rect()
        self.rect.x         = width / 2 
        self.rect.y         = height - size * 2
        self.hop_cooldown   = 20
        self.hop_cooldownX  = self.hop_cooldown
        self.hop_cooldownY  = self.hop_cooldown
        self.count          = 0

    def update(self, width, height, size, jump_distance, movementX = [0,0], movementY = [0,0]): 
        self.out_of_bounds(width, height, size)
        if movementX[0] == True and movementY[0] == False and movementY[1] == False:
            if self.hop_cooldownX == self.hop_cooldown:
                self.hop_cooldownX = 0
                self.rect.x -= jump_distance
            self.hop_cooldownX += 1
        elif movementX[1] == True and movementY[0] == False and movementY[1] == False:
            if self.hop_cooldownX == self.hop_cooldown:
                self.hop_cooldownX = 0
                self.rect.x += jump_distance
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
        if self.rect.y > size * 6:
            if self.rect.x >= width - size:
                self.rect.x = width - size
            elif self.rect.x <= 0:
                    self.rect.x = 0
        if self.rect.y >= height - size * 2:
                self.rect.y = height - size * 2
        elif self.rect.y <= 0:
                self.rect.y = 0
    
    def get_x(self): 
        return self.rect.x 

class Final_Lily(pygame.sprite.Sprite): 
    WIDTH = 20 

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load("./resources/floaters/final_lily_placeholder.png").convert_alpha() 
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
        self.image  = pygame.image.load("./resources/misc/frog_placeholder.png").convert_alpha() 
        self.rect   = self.image.get_rect()
        self.rect.x = x - 6 
        self.rect.y = 32 

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

class Vehicle(pygame.sprite.Sprite): 
    def __init__(self, type, width, height, size, start_x):
        super().__init__()
        self.type = type 
        self.count = 0 
        if type == 'car':
            self.image = pygame.image.load("./resources/vehicles/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 3
            self.velocity = -1
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'car2':
            self.image = pygame.image.load("./resources/vehicles/car_placeholder.png")
            self.rect = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 6
            self.velocity = 1
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor':
            self.image = pygame.image.load("./resources/vehicles/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 4
            self.velocity = 2 
            self.offset = 1 
            self.delay = -self.width * 8 
        if type == 'tractor2':
            self.image = pygame.image.load("./resources/vehicles/tractor_placeholder.png")
            self.rect  = self.image.get_rect()
            self.width = size 
            self.rect.x = start_x
            self.rect.y = height - size * 7
            self.velocity = -2 
            self.offset = 1 
            self.delay = width + self.width * 3 
        if type == 'truck':
            self.image = pygame.image.load("./resources/vehicles/truck_placeholder.png")
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