import pygame

class UI:
    def __init__(self, height):
        self.image = pygame.image.load("./resources/bottom_UI_two_lives.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = height

    def update(self, type):
        if type == '2':
            self.image = pygame.image.load("./resources/bottom_UI_two_lives.png").convert_alpha()
        if type == '1':
            self.image = pygame.image.load("./resources/bottom_UI_one_life.png").convert_alpha()
        if type == '0':
            self.image = self.image = pygame.image.load("./resources/bottom_UI_no_lives.png").convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TopUI:
    def __init__(self):
        self.image = pygame.image.load("./resources/top_UI.png")
        self.rect = self.image.get_rect()
        self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Score:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)
        self.surf = self.font.render('0', False, 'White', None)
        self.rect = self.surf.get_rect()
        self.rect.x = 70

    def draw(self, screen, current_score):
        self.surf = self.font.render(str(current_score), False, 'White', None)
        screen.blit(self.surf,self.rect)

    

class Timer_Bar(pygame.sprite.Sprite):
    def __init__(self, height, size, offset):
        super().__init__()
        self.image = pygame.image.load("./resources/bottom_UI_timer.png")
        self.rect = self.image.get_rect()
        self.rect.x = 90 + offset
        self.rect.y = height - size + 2

    def destroy(self, posX):
        if self.rect.x == posX:
            self.kill()
            return True 
        return False

class Current_Score():
    def __init__(self):
        self.visited_pos = []
        self.collision = False
        self.score = 0
        self.move_forward = 10
        self.frog_saved = 50
        self.level_completed = 1000
    
    def unique_position(self, posY):
        if posY not in self.visited_pos:
            self.visited_pos.append(posY)
            return True
        else:
            return False

    def update_score(self, type, time_left):
        if type == 'stepforward':
            self.score += self.move_forward
        if type == 'frogsaved':
            self.score += self.frog_saved
            self.score += (time_left * 2) * 10
        if type == 'levelcomplete':
            self.score += self.level_completed

class Background: 
    RIVER_SIZE = 5

    def __init__(self, width, height, size): 
        self.safe_platform_image    = pygame.image.load("./resources/safe_platform_placeholder.png").convert_alpha() 
        self.river_image            = pygame.image.load("./resources/river_placeholder.png").convert_alpha() 
        self.finish_platform_image  = pygame.image.load("./resources/finish_platform_placeholder_new.png").convert_alpha() 
        self.width  = width 
        self.height = height
        self.size   = size 

    def draw(self, screen): 
        self.draw_safe_platforms(screen) 
        self.draw_river(screen) 
        self.draw_finish_platform(screen) 

    def draw_safe_platforms(self, screen): 
        self.safe_platform      = self.safe_platform_image.get_rect() 
        self.safe_platform.y    = self.height - self.size * 2
        screen.blit(self.safe_platform_image, self.safe_platform)
        self.safe_platform.y    = self.RIVER_SIZE * self.size + self.size + self.size
        screen.blit(self.safe_platform_image, self.safe_platform)
    
    def draw_river(self, screen): 
        river = self.river_image.get_rect() 
        for i in range(self.RIVER_SIZE + 1): 
            river.y = (i + 1) * self.size 
            screen.blit(self.river_image, river) 

    def draw_finish_platform(self, screen): 
        finish_platform = self.finish_platform_image.get_rect() 
        finish_platform.y  = 0 + self.size
        screen.blit(self.finish_platform_image, finish_platform)