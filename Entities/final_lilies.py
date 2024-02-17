import pygame 

class Final_Lily(pygame.sprite.Sprite): 
    WIDTH = 20 
    LILY_IMG_FILE = "./resources/floaters/final_lily_placeholder.png"
    SAFE_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png"

    def __init__(self, x, y):
        super().__init__()
        self.image          = pygame.image.load(Final_Lily.LILY_IMG_FILE).convert_alpha() 
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
        self.image  = pygame.image.load(Final_Lily.SAFE_LILY_IMG_FILE).convert_alpha()
        self.rect   = self.image.get_rect()
        self.rect.x = x - 6 
        self.rect.y = 32 

    def set_occupied(self): 
        self.occupied = True 
        self.set_safe() 

class Ordinary_Final_Lily(Final_Lily): 

    def __init__(self, x, y):
        super().__init__(x, y)

class Bonus_Final_Lily(Final_Lily): 
    FLY_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)


class Hostile_Final_Lily(Final_Lily): 
    BIRD_LILY_IMG_FILE = "./resources/misc/frog_placeholder.png" #to be replaced 

    def __init__(self, x, y):
        super().__init__(x, y)