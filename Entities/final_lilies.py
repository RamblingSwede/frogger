import pygame 
import threading 

class Final_Lily(pygame.sprite.Sprite): 
    WIDTH = 20 
    LILY_IMG_FILE = "./resources/misc/final_lily_placeholder.png"
    SAFE_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png"
    CURRENT_IMG = LILY_IMG_FILE

    def __init__(self, x, y, timer_delay):
        super().__init__()
        self.image          = pygame.image.load(Final_Lily.LILY_IMG_FILE).convert_alpha() 
        self.rect           = self.image.get_rect()
        self.rect.x         = x
        self.rect.y         = y
        self.occupied       = False
        self.timer          = threading.Timer(timer_delay, self.update_image).start()

    def hit(self, x_left, size): 
        if self.occupied: 
            return False 
        x_right = x_left + size 
        mid = self.rect.x + Final_Lily.WIDTH / 2
        return x_left < mid and x_right > mid 

    def set_safe(self): 
        x            = self.rect.x 
        self.image   = pygame.image.load(Final_Lily.SAFE_LILY_IMG_FILE).convert_alpha()
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
        self.timer = threading.Timer(8, self.update_image).start()



class Ordinary_Final_Lily(Final_Lily): 

    def __init__(self, x, y):
        super().__init__(x, y, 2)

    def set_image(self): 
        return Final_Lily.LILY_IMG_FILE
    


class Bonus_Final_Lily(Final_Lily): 
    FLY_LILY_IMG_FILE = "./resources/misc/fly_final_lily_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y, 2)
        self.active = False 

    def set_image(self): 
        if self.active: 
            self.active = False
            return Final_Lily.LILY_IMG_FILE
        else:
            self.active = True
            return Bonus_Final_Lily.FLY_LILY_IMG_FILE
    


class Hostile_Final_Lily(Final_Lily): 
    BIRD_LILY_IMG_FILE = "./resources/misc/bird_final_lily_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y, 6)
        self.active = False 

    def set_image(self): 
        if self.active: 
            self.active = False
            return Final_Lily.LILY_IMG_FILE
        else:
            self.active = True
            return Hostile_Final_Lily.BIRD_LILY_IMG_FILE