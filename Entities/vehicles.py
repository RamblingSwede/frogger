import pygame

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