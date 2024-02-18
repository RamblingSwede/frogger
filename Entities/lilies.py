import pygame 
import threading 
from random import randint 

class Lily(pygame.sprite.Sprite): 
    WIDTH = 20 
    LILY_IMG_FILE = "./resources/misc/lily_placeholder.png"
    SAFE_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png"
    CURRENT_IMG = LILY_IMG_FILE

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load(Lily.LILY_IMG_FILE).convert_alpha() 
        self.rect           = self.image.get_rect()
        self.rect.x         = x
        self.rect.y         = y
        self.occupied       = False
        self.timer          = threading.Timer(randint(5, 15), self.update_image)
        self.timer.start()

    def is_active(self): 
        return self.active 

    def hit(self, x_left, size): 
        if self.occupied or self.is_hostile(): 
            return False 
        x_right = x_left + size 
        mid = self.rect.x + Lily.WIDTH / 2
        return x_left < mid and x_right > mid 

    def set_safe(self): 
        x            = self.rect.x 
        self.image   = pygame.image.load(Lily.SAFE_LILY_IMG_FILE).convert_alpha()
        self.rect    = self.image.get_rect()
        self.rect.x  = x - 6 
        self.rect.y  = 32

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

    def update_image(self): 
        if not self.occupied: 
            x = self.rect.x 
            y = self.rect.y 
            next_img = self.set_image() 
            self.image = pygame.image.load(next_img)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.reset_timer()

    def reset_timer(self): 
        self.timer = threading.Timer(randint(4, 12), self.update_image)
        self.timer.start()



class Ordinary_Lily(Lily): 

    def __init__(self, x, y):
        super().__init__(x, y)

    def set_image(self): 
        return Lily.LILY_IMG_FILE
    
    def is_hostile(self): 
        return False
    


class Bonus_Lily(Lily): 
    FLY_LILY_IMG_FILE = "./resources/misc/fly_lily_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False 

    def set_image(self): 
        if self.active: 
            self.active = False
            return Lily.LILY_IMG_FILE
        else:
            self.active = True
            return Bonus_Lily.FLY_LILY_IMG_FILE
        
    def is_hostile(self): 
        return False
    


class Hostile_Lily(Lily): 
    BIRD_LILY_IMG_FILE = "./resources/misc/bird_lily_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False 

    def set_image(self): 
        if self.active: 
            self.active = False
            return Lily.LILY_IMG_FILE
        else:
            self.active = True
            return Hostile_Lily.BIRD_LILY_IMG_FILE
        
    def is_hostile(self): 
        return self.active