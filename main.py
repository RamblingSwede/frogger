from sprite_generator import *
from sprite_controller import *
from Entities.vehicles import *
from Entities.floaters import *
from Entities.frogs import *
from Entities.lilies import *
from utils import *
from view import UI
import pygame
import sys

# Grodan kommer inte tillbaka när loggen går ut ur bild - Gammal kommentar? Kan inte reproducera

BLOCK_SIZE = 32
SCREEN_WIDTH, SCREEN_HEIGHT = BLOCK_SIZE * 14, BLOCK_SIZE * 15
RIVER_Y = (BLOCK_SIZE, BLOCK_SIZE * 7)
FPS = 60
LEFT_DIR    = [pygame.K_a, pygame.K_LEFT]
RIGHT_DIR   = [pygame.K_d, pygame.K_RIGHT]
UP_DIR      = [pygame.K_w, pygame.K_UP]
DOWN_DIR    = [pygame.K_s, pygame.K_DOWN]

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger - Level 1')
        self.level              = 1
        self.clock              = pygame.time.Clock()
        self.ui                 = UI(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE)
        self.current_score      = CurrentScore()
        self.high_score         = Highscore()
        self.in_start_screen    = True
        self.running            = False
        self.safe_frogs         = 0
        self.lives_left         = 2
        self.sprite_controller  = SpriteController(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, RIVER_Y)
        self.timer              = pygame.USEREVENT + 1

        pygame.time.set_timer(self.timer, 30000)
        self.movementX          = [False, False]
        self.movementY          = [False, False]
        self.jump_distance      = BLOCK_SIZE
        self.start_time         = int(pygame.time.get_ticks() / 1000)

    def timer_tick(self, time):
        self.ui.update_timer(time)

    def set_jump_distance(self, platform): 
        dists = platform.get_jump_distance() 
        if self.movementX[0]: 
            self.jump_distance = dists[0] 
        elif self.movementX[1]: 
            self.jump_distance = dists[1] 
    
    def handle_reached_final_lily(self, lily, frog, friend_frog):
        if self.safe_frogs == 4:
            if isinstance(lily, BonusLily) and lily.is_active(): 
                self.current_score.update_score('frogsavedbonus',  self.current_time)
            elif frog.sprite.carrying_friend():
                self.current_score.update_score('frogsavedbonus',  self.current_time)
                friend_frog.sprite.set_safe()
            else: 
                self.current_score.update_score('frogsaved',  self.current_time)
            self.current_score.update_score('levelcomplete',  self.current_time)
            self.level_completed()
        else:
            self.current_score.visited_pos.clear()
            self.safe_frogs += 1
            if isinstance(lily, BonusLily) and lily.is_active(): 
                self.current_score.update_score('frogsavedbonus',  self.current_time)
            elif frog.sprite.carrying_friend():
                self.current_score.update_score('frogsavedbonus',  self.current_time)
                friend_frog.sprite.set_safe()
            else: 
                self.current_score.update_score('frogsaved',  self.current_time)
            self.respawn()

    def lose_life(self): 
        if self.movementY[1]:
            self.current_score.score -= 10
            self.current_score.visited_pos.pop()
        if self.lives_left > 0:
            self.lives_left -= 1
            self.respawn()
        else:
            pygame.time.set_timer(self.timer, 30000)
            self.start_time = int(pygame.time.get_ticks() / 1000)
            self.running = False

    def respawn(self):
        pygame.time.set_timer(self.timer, 30000)
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.sprite_controller.handle_frog_respawn()
        self.ui.respawn(self.lives_left)
    
    def reset_game(self):
        self.running = True
        self.current_score.visited_pos.clear()
        pygame.display.set_caption('Frogger - Level ' + str(self.level))
        self.sprite_controller.kill_sprites()
        self.reset_movements()
        self.sprite_controller.reset(self.level)
        self.ui.reset_timer_bar()

    def reset_movements(self):
        self.movementX = [False, False]
        self.movementY = [False, False]

    def level_completed(self):
        print('Level completed')
        if int(self.current_score.score) > int(self.high_score.score):
            self.high_score.update(self.current_score.score)
        self.high_score.refresh()
        self.level += 1
        self.safe_frogs = 0
        self.reset_game()
        self.respawn()
                    
    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.ui.update_display()
        self.sprite_controller.update_display(self.ui.get_screen(), self.jump_distance, self.movementX, self.movementY)
        self.current_score.draw(self.ui.get_screen(), self.current_score.score)
        self.high_score.draw(self.ui.get_screen())

    def start_screen(self):
        self.ui.draw_start_screen()
        self.current_score.draw(self.ui.get_screen(), self.current_score.score)
        self.high_score.draw(self.ui.get_screen())
        pygame.display.update()  

    def starting_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sprite_controller.kill_lilies()
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.current_score.score = 0
                self.safe_frogs = 0
                self.lives_left = 2
                self.level = 1
                self.reset_game()
                self.respawn()
                self.in_start_screen = False
                self.running = True    
    
    def run(self):
        self.start_screen()  
        while True:
            while self.in_start_screen:
                self.ui.update_splash_screen()
                pygame.display.update()
                self.starting_event()
            while not self.in_start_screen:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        mx, my = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.running and mx >= 160 and mx <= 220 and my >= 264 and my <= 294:
                        self.ui.update_respawn_menu("9")
                        self.current_score.score = 0
                        self.safe_frogs = 0
                        self.lives_left = 2
                        self.level = 1
                        self.reset_game()
                        self.respawn()
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.running and mx >= 235 and mx <= 300 and my >= 264 and my <= 294:
                        self.ui.update_respawn_menu("9")
                        self.current_score.score = 0
                        self.in_start_screen = True
                        self.start_screen()
                    if event.type == pygame.QUIT:
                        self.sprite_controller.kill_lilies()
                        pygame.quit()
                        sys.exit()       
                    if event.type == pygame.KEYDOWN:
                        if event.key in LEFT_DIR:
                            self.movementX[0] = True
                        if event.key in RIGHT_DIR:
                            self.movementX[1] = True
                        if event.key in UP_DIR:
                            self.movementY[1] = True
                            if self.current_score.unique_position(self.sprite_controller.get_frog().sprite.rect.y):
                                self.current_score.update_score('stepforward', self.current_time)
                        if event.key in DOWN_DIR:
                            self.movementY[0] = True
                        if event.key == pygame.K_SPACE:
                            self.level_completed()
                            ##Only exists for debug, to be replaced with restart menu at some point
                            #self.current_score.score = 0
                            #self.safe_frogs = 0
                            #self.lives_left = 2
                            #self.level = 1
                            #self.reset_game()
                            #self.respawn()
                    if event.type == pygame.KEYUP:
                        if event.key in LEFT_DIR:
                            self.movementX[0] = False
                        if event.key in RIGHT_DIR:
                            self.movementX[1] = False
                        if event.key in UP_DIR:
                            self.movementY[1] = False
                        if event.key in DOWN_DIR:
                            self.movementY[0] = False
                    if event.type == self.timer and self.running:
                        self.lose_life()

                if self.running:
                    self.sprite_controller.unknown_lily_action()
                    self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
                    self.timer_tick(pygame.time.get_ticks() / 1000 - self.start_time)
                    self.sprite_controller.handle_collisions(self)
                    self.update_display() 
                    pygame.display.update()
                    self.clock.tick(FPS)
                
                if not self.running and not self.in_start_screen:
                    self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
                    self.timer_tick(pygame.time.get_ticks() / 1000 - self.start_time)                  
                    if 10 - self.current_time > 0:
                        self.ui.update_respawn_menu(str(10 - self.current_time), True)
                    else:
                        self.ui.update_respawn_menu("9")
                        self.current_score.score = 0
                        self.in_start_screen = True
                        self.start_screen()
                    pygame.display.update()
Game().run()