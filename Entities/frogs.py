import pygame

class Frog(pygame.sprite.Sprite):
    def __init__(self, image, x, y): 
        super().__init__()
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.count = 0 

    def match_speed(self, offset, velocity):
        if self.count == offset: 
            self.rect.x += velocity
            self.count = 0 
        if self.count >= 3:
            self.count = 0
        self.count += 1 
     


class FriendFrog(Frog): 
    def __init__(self, frog, log):
        super().__init__("./resources/misc/friend_frog_placeholder.png", log.get_pos()[0], log.get_pos()[1])
        self.is_on_log  = True
        self.is_carried = False
        self.safe    = False
        self.log        = log
        self.frog       = frog

    def hit(self, size): 
        y = self.frog.sprite.get_y()
        x_left = self.frog.sprite.get_x()
        x_right = x_left + size 
        mid = self.rect.x + size / 2
        return y == self.rect.y and x_left < mid and x_right > mid 

    def update(self):
        if self.is_on_log:
            pos = self.log.get_pos()
            self.rect.x = pos[0]
            self.rect.y = pos[1]
        elif self.is_carried:
            self.rect.x = self.frog.sprite.get_x()
            self.rect.y = self.frog.sprite.get_y()
    
    def set_carried(self): 
        self.is_on_log = False
        self.is_carried = True

    def set_safe(self): 
        self.safe = True
        self.is_carried = False
        self.is_on_log = False
        self.rect.x = -100
        self.rect.y = -100

    def is_safe(self):
        return self.safe



class NormalFrog(Frog): 
    def __init__(self, width, height, size):
        super().__init__("./resources/misc/frog_placeholder.png", width / 2, height - size * 2)
        self.carrying       = False
        self.hop_cooldown   = 20
        self.hop_cooldownX  = self.hop_cooldown
        self.hop_cooldownY  = self.hop_cooldown

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
    
    def get_y(self):
        return self.rect.y
    
    def carrying_friend(self): 
        return self.carrying
    
    def set_carry_friend(self, carrying): 
        self.carrying = carrying
    