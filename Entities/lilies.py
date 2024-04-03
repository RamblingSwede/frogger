import os
import pygame 
import threading 
from random import randint 

class Lily(pygame.sprite.Sprite): 
    WIDTH = 20 
    LILY_IMG_FILE = "./resources/misc/lily.png"
    SAFE_LILY_IMG_FILE = "./resources/misc/safe_frog.png"
    CURRENT_IMG = LILY_IMG_FILE

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load(Lily.LILY_IMG_FILE).convert_alpha() 
        self.rect           = self.image.get_rect()
        self.rect.x         = x
        self.rect.y         = y
        self.occupied       = False

    def is_active(self): 
        return self.active 

    def hit(self, x_left, size): 
        if self.occupied or self.is_hostile(): 
            return False 
        x_right = x_left + size 
        mid = self.rect.x + Lily.WIDTH / 2
        return x_left < mid and x_right > mid 

    def set_safe(self): 
        x           = self.rect.x 
        y           = self.rect.y
        self.image  = pygame.image.load(Lily.SAFE_LILY_IMG_FILE).convert_alpha()
        self.rect   = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

    def start_timer(self):
        self.timer = threading.Timer(randint(5, 15), self.update_image)
        self.timer.start()

    def update_image(self): 
        if not self.occupied: 
            x = self.rect.x 
            y = self.rect.y 
            next_img = self.set_image() 
            self.image = pygame.image.load(next_img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.reset_timer()

    def reset_timer(self): 
        self.timer = threading.Timer(randint(4, 12), self.update_image)
        self.timer.start()

    def kill_thread(self):
        os._exit(1)

class Ordinary_Lily(Lily): 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.test = False

    def set_image(self): 
        return Lily.LILY_IMG_FILE
    
    def is_hostile(self): 
        return False

class Bonus_Lily(Lily): 
    FLY_LILY_IMG_FILE = "./resources/misc/fly_lily.png" 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False 
        self.test = False

    def set_image(self): 
        self.test = False
        if self.active: 
            self.active = False
            self.test = True
            return Lily.LILY_IMG_FILE
        else:
            self.active = True
            return Bonus_Lily.FLY_LILY_IMG_FILE
        
    def is_hostile(self): 
        return False
        
class Crocodile_Lily(Lily):
    CROC_LILY_IMG_FILE = "./resources/misc/crocodile_lily.png"
    CROC_LURK_LILY_IMG_FILE = "./resources/misc/crocodile_lurk_lily.png"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.lurking = False
        self.hunting = False
        self.test = False

    def start_timer(self):
        self.timer = threading.Timer(randint(4, 12), self.update_image)
        self.timer.start()

    def update_image(self): 
        if not self.occupied: 
            x = self.rect.x 
            y = self.rect.y 
            next_img = self.set_image() 
            self.image = pygame.image.load(next_img).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    def reset_timer(self, delay=8): 
        self.timer = threading.Timer(delay, self.update_image)
        self.timer.start()

    def set_image(self): 
        if self.lurking: 
            self.lurking = False
            self.hunting = True
            self.reset_timer(2)
            return Crocodile_Lily.CROC_LILY_IMG_FILE
        elif self.hunting:
            self.hunting = False
            self.reset_timer()
            self.test = True
            return Lily.LILY_IMG_FILE
        else:
            self.lurking = True
            self.reset_timer(2)
            return Crocodile_Lily.CROC_LURK_LILY_IMG_FILE
        
    def is_hostile(self): 
        return self.hunting