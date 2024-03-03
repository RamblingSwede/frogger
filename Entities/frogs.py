import pygame
import threading

from Entities.floaters import Log 

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

    def get_x(self):
        return self.rect.x
    
    def get_y(self):
        return self.rect.y
     


class FriendFrog(Frog):
    def __init__(self, size, frog, log):
        super().__init__("./resources/misc/friend_frog.png", log.get_pos()[0], log.get_pos()[1])
        self.size       = size
        self.is_on_log  = True
        self.is_carried = False
        self.safe       = False
        self.log        = log
        self.frog       = frog
        self.right_dir  = True
        self.delay      = 1.5
        self.timer      = threading.Timer(self.delay, self.jump)
        self.timer.start()

    def hit(self): 
        y = self.frog.sprite.get_y()
        x_left = self.frog.sprite.get_x()
        x_right = x_left + self.size 
        mid = self.rect.x + self.size / 2
        return y == self.rect.y and x_left < mid and x_right > mid 

    def update(self, screen_width, floaters):
        if self.is_on_log:
            pos = self.log.get_pos()
            self.rect.y = pos[1]
            if self.right_dir:
                self.rect.x = pos[0]
            else:
                self.rect.x = pos[0]  + self.size
        elif self.is_carried:
            self.rect.x = self.frog.sprite.get_x()
            self.rect.y = self.frog.sprite.get_y()
        if self.rect.x >= screen_width + self.size / 2: 
            self.inactivate()

    def jump(self): 
        if self.is_on_log:
            pos = self.log.get_pos()
            if self.right_dir:
                self.rect.x = pos[0]
                self.right_dir = False
            else:
                self.rect.x = pos[0] + self.size
                self.right_dir = True
        self.timer = threading.Timer(self.delay, self.jump)
        self.timer.start()
            
    
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
    
    def reset(self, log):
        self.log = log
        self.safe = False
        self.is_carried = False
        self.is_on_log = True

    def inactivate(self):
        self.is_on_log = False
        self.is_carried = False
        self.rect.x = -100
        self.rect.y = -100

    def out_of_bounds(self):
        return (not self.is_on_log) and (not self.is_carried) and (not self.safe)



class NormalFrog(Frog): 
    def __init__(self, width, height, size):
        super().__init__("./resources/misc/frog.png", width / 2, height - size * 2)
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
    
    def carrying_friend(self): 
        return self.carrying
    
    def set_carry_friend(self, carrying): 
        self.carrying = carrying
    