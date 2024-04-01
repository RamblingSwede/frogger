import pygame

class UI:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen             = pygame.display.set_mode((screen_width, screen_height))
        self.background         = Background()
        self.bottom_panel       = BottomPanel(screen_height - block_size)
        self.respawn_menu       = RespawnMenu(screen_width, screen_height)
        self.splash_screen      = SplashScreen()
        self.timer_bar          = TimerBar(screen_width, screen_height, block_size)

    def get_screen(self):
        return self.screen

    def respawn(self, lives_left):
        self.reset_timer_bar()
        self.bottom_panel.update(str(lives_left))

    def reset_timer_bar(self):
        self.timer_bar.reset_timer_bar()

    def draw_start_screen(self):
        self.draw_background()
        self.update_splash_screen()
        self.reset_timer_bar()
        pygame.display.update() 

    def draw_background(self):
        self.screen.fill('Black')
        self.background.draw(self.screen)

    def update_display(self):
        self.draw_background()
        self.bottom_panel.draw(self.screen)
        self.timer_bar.draw2(self.screen)

    def update_respawn_menu(self, sec_left, draw=False):
        self.respawn_menu.update(sec_left, self.screen, draw)

    def update_splash_screen(self):
        self.splash_screen.update()
        self.splash_screen.draw(self.screen)

    def update_timer(self, time):
        self.timer_bar.update(time)



class Background: 
    def __init__(self):
        self.image = pygame.image.load("resources/misc/background.png").convert_alpha()
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class BottomPanel:
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



class RespawnMenu:
    def __init__(self, width, height):
        self.image = pygame.image.load("./resources/ui/game_over_9.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = height // 3.5
        self.rect.x = width // 3

    def update(self, type, screen, draw):
        if type >= '9':
            self.image = pygame.image.load("./resources/ui/game_over_9.png").convert_alpha()
        elif type == '8':
            self.image = pygame.image.load("./resources/ui/game_over_8.png").convert_alpha()
        elif type == '7':
            self.image = pygame.image.load("./resources/ui/game_over_7.png").convert_alpha()
        elif type == '6':
            self.image = pygame.image.load("./resources/ui/game_over_6.png").convert_alpha()
        elif type == '5':
            self.image = pygame.image.load("./resources/ui/game_over_5.png").convert_alpha()
        elif type == '4':
            self.image = pygame.image.load("./resources/ui/game_over_4.png").convert_alpha()
        elif type == '3':
            self.image = pygame.image.load("./resources/ui/game_over_3.png").convert_alpha()
        elif type == '2':
            self.image = pygame.image.load("./resources/ui/game_over_2.png").convert_alpha()
        elif type == '1':            
            self.image = pygame.image.load("./resources/ui/game_over_1.png").convert_alpha()
        if draw:
            self.draw(screen)
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)



class SplashScreen:
    def __init__(self):
        self.image = pygame.image.load("./resources/ui/splash_screen.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = 0
        self.animation_index = 0
        self.timer = 0

    def update(self):
        self.images = [pygame.image.load(img) for img in [
        "./resources/ui/splash_screen.png", "./resources/ui/splash_screen.png", "./resources/ui/splash_screen.png", 
        "./resources/ui/splash_screen.png", "./resources/ui/splash_screen.png", "./resources/ui/splash_screen_grey.png",
        "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", 
        "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", 
        "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", 
        "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_black.png", "./resources/ui/splash_screen_grey.png"]]
        self.timer += 1
        if self.timer >= 1:
            self.timer = 0
            self.image = self.images[self.animation_index]
            self.animation_index += 1
            if self.animation_index == len(self.images):
                self.animation_index = 0

    def draw(self, screen):
       screen.blit(self.image, self.rect)



class TimerBar:
    GREEN = (106, 190, 48)
    def __init__(self, screen_width, screen_height, block_size):
        super().__init__()
        self.total_time     = 30
        self.screen_width   = screen_width
        self.screen_height  = screen_height
        self.block_size     = block_size
        self.reset_timer_bar()

    def update(self, time):
        offset = (self.total_time - time) / self.total_time
        dx = self.width * (1 - offset)
        self.bar = pygame.Rect(self.x, self.y, self.width - dx, self.height)

    def draw2(self, display): 
        pygame.draw.rect(display, TimerBar.GREEN, self.bar)
        return True
    
    def reset_timer_bar(self):
        self.x          = 90
        self.y          = self.screen_height - self.block_size + 2
        self.width      = self.screen_width - self.x - 2
        self.height     = self.block_size / 2
        self.bar        = pygame.Rect(self.x, self.y, self.width, self.height)

    def destroy(self):
        self.bar = pygame.Rect(0, 0, 0, 0)