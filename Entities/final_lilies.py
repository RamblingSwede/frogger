import pygame 
import threading 

class Final_Lily(pygame.sprite.Sprite): 
    WIDTH = 20 
    LILY_IMG_FILE = "./resources/floaters/final_lily_placeholder.png"
    SAFE_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png"
    CURRENT_IMG = LILY_IMG_FILE

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load(Final_Lily.LILY_IMG_FILE).convert_alpha() 
        self.rect           = self.image.get_rect()
        self.rect.x         = x
        self.rect.y         = y
        self.occupied       = False
        self.timer          = threading.Timer(8, self.update())

    def hit(self, x_left, size): 
        if self.occupied: 
            return False 
        x_right = x_left + size 
        mid = self.rect.x + Final_Lily.WIDTH / 2
        return x_left < mid and x_right > mid 

    def set_safe(self): 
        x           = self.rect.x 
        self.image  = pygame.image.load(Final_Lily.SAFE_LILY_IMG_FILE).convert_alpha()
        self.rect   = self.image.get_rect()
        self.rect.x = x - 6 
        self.rect.y = 32 

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

    def update(self): 
        if not self.occupied: 
            next_img = self.update_image() 
            self.image = pygame.image.load(next_img).convert_alpha() 
            self.rect = self.image.get_rect()



class Ordinary_Final_Lily(Final_Lily): 

    def __init__(self, x, y):
        super().__init__(x, y)

    def update_image(self): 
        return super().LILY_IMG_FILE
    


class Bonus_Final_Lily(Final_Lily): 
    FLY_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False 

    def update_image(self): 
        if super().CURRENT_IMG == super().SAFE_LILY_IMG_FILE:
            return super().CURRENT_IMG
        if self.active: 
            self.active = False
            return super().LILY_IMG_FILE
        else:
            self.active = True
            return Bonus_Final_Lily.FLY_LILY_IMG_FILE
    


class Hostile_Final_Lily(Final_Lily): 
    BIRD_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)
        self.active = False 

    def update_image(self): 
        if super().CURRENT_IMG == super().SAFE_LILY_IMG_FILE:
            return super().CURRENT_IMG
        if self.active: 
            self.active = False
            return super().LILY_IMG_FILE
        else:
            self.active = True
            return Hostile_Final_Lily.BIRD_LILY_IMG_FILE