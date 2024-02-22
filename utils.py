import pygame

class UI:
    def __init__(self, height):
        self.image = pygame.image.load("./resources/ui/bottom_UI_two_lives.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = height

    def update(self, type):
        if type == '2':
            self.image = pygame.image.load("./resources/ui/bottom_UI_two_lives.png").convert_alpha()
        if type == '1':
            self.image = pygame.image.load("./resources/ui/bottom_UI_one_life.png").convert_alpha()
        if type == '0':
            self.image = pygame.image.load("./resources/ui/bottom_UI_no_lives.png").convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class TopUI:
    def __init__(self):
        self.image = pygame.image.load("./resources/ui/top_UI.png")
        self.rect = self.image.get_rect()
        self.rect.y = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Timer_Bar():
    GREEN = (106, 190, 48)
    def __init__(self, x, y, width, height):
        super().__init__()
        self.total_time = 30
        self.x          = x
        self.y          = y
        self.width      = width
        self.height     = height
        self.bar        = pygame.Rect(x, y, width, height)

    def update(self, time):
        offset = (self.total_time - time) / self.total_time
        dx = self.width * (1 - offset)
        self.bar = pygame.Rect(self.x, self.y, self.width - dx, self.height)

    def draw2(self, display): 
        pygame.draw.rect(display, Timer_Bar.GREEN, self.bar)
        return True

    def destroy(self):
        self.bar = pygame.Rect(0, 0, 0, 0)

class Current_Score():
    def __init__(self):
        self.font = pygame.font.SysFont(None, 30)
        self.surf = self.font.render('0', False, 'White', None)
        self.rect = self.surf.get_rect()
        self.rect.x = 70

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

    def update_score(self, type, elapsed_time):
        print(elapsed_time)
        if type == 'stepforward':
            self.score += self.move_forward
        elif type == 'frogsaved':
            self.score += self.frog_saved
            self.score += ((30 - elapsed_time) * 2) * 10
            print(((30 - elapsed_time) * 2) * 10)
        elif type == 'frogsavedbonus':
            self.score += self.frog_saved
            self.score += ((60 - elapsed_time) * 2) * 10 #How many points should bonus give? 
        elif type == 'levelcomplete':
            self.score += self.level_completed

    def draw(self, screen, current_score):
        self.surf = self.font.render(str(current_score), False, 'White', None)
        screen.blit(self.surf,self.rect)

class Highscore:
    def __init__(self):
        self.file = './resources/documents/highscore.txt'
        self.font = pygame.font.SysFont(None, 30)
        self.score = ''
        self.surf = ''
        self.rect = ''
        self.refresh()

    def refresh(self):
        try:
            with open(self.file, 'r+', encoding = 'utf-8') as file:
                self.score = file.read()
                self.surf = self.font.render(self.score, False, 'White', None)
                self.rect = self.surf.get_rect()
                self.rect.x = 325
                
        except:
            with open(self.file, 'w+', encoding = 'utf-8') as file:
                file.write("0")  
    
    def update(self, current_score):
        with open(self.file, 'w+', encoding = 'utf-8') as file:
            file.write(str(current_score))  

    def draw(self, screen):
        screen.blit(self.surf,self.rect)
        
class RespawnMenu:
    def __init__(self, width, height):
        self.image = pygame.image.load("./resources/ui/game_over_9.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = height // 3.5
        self.rect.x = width // 3

    def update(self, type):
        if type >= '9':
            self.image = pygame.image.load("./resources/ui/game_over_9.png").convert_alpha()
        if type == '8':
            self.image = pygame.image.load("./resources/ui/game_over_8.png").convert_alpha()
        if type == '7':
            self.image = pygame.image.load("./resources/ui/game_over_7.png").convert_alpha()
        if type == '6':
            self.image = pygame.image.load("./resources/ui/game_over_6.png").convert_alpha()
        if type == '5':
            self.image = pygame.image.load("./resources/ui/game_over_5.png").convert_alpha()
        if type == '4':
            self.image = pygame.image.load("./resources/ui/game_over_4.png").convert_alpha()
        if type == '3':
            self.image = pygame.image.load("./resources/ui/game_over_3.png").convert_alpha()
        if type == '2':
            self.image = pygame.image.load("./resources/ui/game_over_2.png").convert_alpha()
        if type == '1':            
            self.image = pygame.image.load("./resources/ui/game_over_1.png").convert_alpha()
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class SplashScreen:
    def __init__(self):
        self.image = pygame.image.load("./resources/ui/splash_screen.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Background: 
    RIVER_SIZE = 5

    def __init__(self, width, height, size): 
        self.safe_platform_image    = pygame.image.load("./resources/misc/safe_platform_placeholder.png").convert_alpha() 
        self.river_image            = pygame.image.load("./resources/misc/river_placeholder.png").convert_alpha() 
        self.finish_platform_image  = pygame.image.load("./resources/misc/finish_platform_placeholder_new.png").convert_alpha() 
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