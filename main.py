from Entities.spriteGenerator import spriteGenerator
from Entities.vehicles import *
from Entities.floaters import *
from Entities.frogs import *
from Entities.lilies import *
from utils import *
from random import randint
import pygame
import sys

# Grodan kommer inte tillbaka när loggen går ut ur bild

BLOCK_SIZE = 32
SCREEN_WIDTH, SCREEN_HEIGHT = BLOCK_SIZE * 14, BLOCK_SIZE * 15
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
        self.screen             = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background         = Background()
        self.ui                 = UI(SCREEN_HEIGHT - BLOCK_SIZE)
        self.respawn_menu       = RespawnMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.current_score      = Current_Score()
        self.high_score         = Highscore()
        self.splash_screen      = SplashScreen()
        self.in_start_screen    = True
        self.running            = False
        self.safe_frogs         = 0
        self.lives_left         = 2
        self.floater_group      = pygame.sprite.Group()
        self.vehicle_group      = pygame.sprite.Group()
        self.sprite_generator   = spriteGenerator(BLOCK_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.lilies_group       = pygame.sprite.Group()
        self.frog               = pygame.sprite.GroupSingle()
        self.frog.add(NormalFrog(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE))
        self.friend_frog        = pygame.sprite.GroupSingle()
        self.timer              = pygame.USEREVENT + 1

        pygame.time.set_timer(self.timer, 30000)
        self.movementX          = [False, False]
        self.movementY          = [False, False]
        self.jump_distance      = BLOCK_SIZE
        self.start_time         = int(pygame.time.get_ticks() / 1000)

    def spawn_lilies(self, level):
        y = BLOCK_SIZE + BLOCK_SIZE / 4 + 2
        x = 19
        if level == 1:
            for i in range(5):
                x = 19 + i * BLOCK_SIZE * 3
                random_nbr = randint(1, 14)
                if random_nbr < 4:
                    print("Bonus lily")
                    self.lilies_group.add(Bonus_Lily(x, y))
                else:
                    print("Ordinary lily")
                    self.lilies_group.add(Ordinary_Lily(x, y))
        if level == 2:
            for i in range(1, 5):
                x = 19 + i * BLOCK_SIZE * 3
                random_nbr = randint(1, 14)
                if random_nbr < 5:
                    print("Bonus lily")
                    self.lilies_group.add(Bonus_Lily(x, y))
                elif random_nbr < 11:
                    print("Croc lily")
                    self.lilies_group.add(Crocodile_Lily(x, y))
                else:
                    print("Ordinary lily")
                    self.lilies_group.add(Ordinary_Lily(x, y))
        if level >= 3:
            for i in range(1, 5):
                x = 19 + i * BLOCK_SIZE * 3
                random_nbr = randint(1, 14)
                if random_nbr < 3:
                    print("Bonus lily")
                    self.lilies_group.add(Bonus_Lily(x, y))
                elif random_nbr < 11:
                    print("Croc lily")
                    self.lilies_group.add(Crocodile_Lily(x, y))
                else:
                    print("Ordinary lily")
                    self.lilies_group.add(Ordinary_Lily(x, y))

    def spawn_timer_bar(self):
        self.timer_bar = Timer_Bar(90, SCREEN_HEIGHT - BLOCK_SIZE + 2, SCREEN_WIDTH - 90 - 2, BLOCK_SIZE / 2)

    def timer_tick(self, time):
        self.timer_bar.update(time)

    def collision(self):
        self.handle_vehicle_hit() 
        self.handle_floater_hit() 
        self.handle_final_platform_hit() 

    def handle_vehicle_hit(self): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.vehicle_group, False):
            self.lose_life() 

    def handle_floater_hit(self): 
        if self.in_river():
            if pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False):
                platforms = pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False)
                for platform in platforms:
                    if platform.within_bounds(self.frog.sprite.rect.x, BLOCK_SIZE): 
                        if platform.hostile(self.frog.sprite):
                            self.lose_life()
                            break
                        self.set_jump_distance(platform) 
                        self.frog.sprite.match_speed(platform.offset, platform.velocity)
                        self.handle_friend_frog_hit()
                    else:
                        self.lose_life() 
            else:
                self.lose_life() 
        else: 
            self.jump_distance = BLOCK_SIZE 

    def handle_friend_frog_hit(self):
        if self.frog.sprite.carrying_friend() or self.friend_frog.sprite.is_safe():
            return
        try: 
            if self.friend_frog.sprite.hit():
                self.frog.sprite.set_carry_friend(True)
                self.friend_frog.sprite.set_carried()
        except Exception as e: 
            print("Friend frog is no more: ", e)

    def handle_final_platform_hit(self): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.lilies_group, False): 
            lily = pygame.sprite.spritecollide(self.frog.sprite, self.lilies_group, False)[0] 
            if lily.hit(self.frog.sprite.get_x(), BLOCK_SIZE): 
                lily.set_occupied() 
                if self.safe_frogs == 4:
                    if isinstance(lily, Bonus_Lily) and lily.is_active(): 
                        self.current_score.update_score('frogsavedbonus',  self.current_time)
                    elif self.frog.sprite.carrying_friend():
                        self.current_score.update_score('frogsavedbonus',  self.current_time)
                        self.friend_frog.sprite.set_safe()
                    else: 
                        self.current_score.update_score('frogsaved',  self.current_time)
                    self.current_score.update_score('levelcomplete',  self.current_time)
                    self.level_completed()
                else:
                    self.current_score.visited_pos.clear()
                    self.safe_frogs += 1
                    if isinstance(lily, Bonus_Lily) and lily.is_active(): 
                        self.current_score.update_score('frogsavedbonus',  self.current_time)
                    elif self.frog.sprite.carrying_friend():
                        self.current_score.update_score('frogsavedbonus',  self.current_time)
                        self.friend_frog.sprite.set_safe()
                    else: 
                        self.current_score.update_score('frogsaved',  self.current_time)
                    print('Frog made it to safety')
                    self.respawn()
            else: 
                print('Didn\'t hit')
                self.lose_life() 
        elif self.frog.sprite.rect.y == BLOCK_SIZE:
            self.lose_life() 

    def set_jump_distance(self, platform): 
        dists = platform.get_jump_distance() 
        if self.movementX[0]: 
            self.jump_distance = dists[0] 
        elif self.movementX[1]: 
            self.jump_distance = dists[1] 


    def in_river(self): 
        return self.frog.sprite.rect.y < BLOCK_SIZE * 7 and self.frog.sprite.rect.y > BLOCK_SIZE

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
        self.timer_bar.destroy()
        if self.frog.sprite.carrying_friend():
            self.frog.sprite.set_carry_friend(False)
            if self.friend_frog.sprite.is_safe():
                self.friend_frog.sprite.set_safe()
            else:
                self.friend_frog.sprite.inactivate()
        self.frog.sprite.rect.x = SCREEN_WIDTH / 2
        self.frog.sprite.rect.y = SCREEN_HEIGHT - BLOCK_SIZE * 2
        self.spawn_timer_bar()
        self.ui.update(str(self.lives_left))
    
    def reset_game(self):
        self.running = True
        self.current_score.visited_pos.clear()
        pygame.display.set_caption('Frogger - Level ' + str(self.level))
        for vehicle in self.vehicle_group:
            vehicle.kill()
        for floater in self.floater_group:
            floater.kill()
        for lily in self.lilies_group:
            lily.kill()
        self.timer_bar.destroy()
        try: 
            self.friend_frog.sprite.kill()
        except Exception as e: 
            print("Friend frog is already dead:", e)
        self.reset_movements()
        self.spawn_lilies(self.level)
        self.sprite_generator.spawn_floaters(self.floater_group, self.frog, self.friend_frog, self.level)
        self.sprite_generator.spawn_vehicles(self.vehicle_group, self.level)
        for lily in self.lilies_group:
            lily.start_timer()
        self.spawn_timer_bar()

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

    def draw_snake(self):
        for floater in self.floater_group:
            if isinstance(floater, SnakeLog):
                floater.draw(self.screen)
                break
                    
    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen)
        self.vehicle_group.update(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, self.vehicle_group)
        self.vehicle_group.draw(self.screen)
        self.floater_group.update(SCREEN_WIDTH, self.floater_group, self.friend_frog)
        self.floater_group.draw(self.screen)
        self.draw_snake()
        self.lilies_group.draw(self.screen) 
        self.frog.update(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, self.jump_distance, self.movementX, self.movementY)
        self.frog.draw(self.screen)
        self.friend_frog.update(SCREEN_WIDTH, self.floater_group)
        self.friend_frog.draw(self.screen)
        self.ui.draw(self.screen)
        self.timer_bar.draw2(self.screen)
        self.current_score.draw(self.screen, self.current_score.score)
        self.high_score.draw(self.screen)

    def start_screen(self):
        self.screen.fill('Black')
        self.background.draw(self.screen)
        self.current_score.draw(self.screen, self.current_score.score)
        self.high_score.draw(self.screen)
        self.splash_screen.update()
        self.splash_screen.draw(self.screen)
        self.spawn_timer_bar()
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for lily in self.lilies_group:
                            lily.kill_thread()
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
        while True:
            while self.in_start_screen:
                self.start_screen()  
            while not self.in_start_screen:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEMOTION:
                        mx, my = pygame.mouse.get_pos()
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.running and mx >= 160 and mx <= 220 and my >= 264 and my <= 294:
                        self.respawn_menu.update("9")
                        self.current_score.score = 0
                        self.safe_frogs = 0
                        self.lives_left = 2
                        self.level = 1
                        self.reset_game()
                        self.respawn()
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.running and mx >= 235 and mx <= 300 and my >= 264 and my <= 294:
                        self.respawn_menu.update("9")
                        self.in_start_screen = True
                    if event.type == pygame.QUIT:
                        for lily in self.lilies_group:
                            lily.kill_thread()
                        pygame.quit()
                        sys.exit()       
                    if event.type == pygame.KEYDOWN:
                        if event.key in LEFT_DIR:
                            self.movementX[0] = True
                        if event.key in RIGHT_DIR:
                            self.movementX[1] = True
                        if event.key in UP_DIR:
                            self.movementY[1] = True
                            if self.current_score.unique_position(self.frog.sprite.rect.y):
                                self.current_score.update_score('stepforward', self.current_time)
                        if event.key in DOWN_DIR:
                            self.movementY[0] = True
                        if event.key == pygame.K_SPACE:
                            ##Only exists for debug, to be replaced with restart menu at some point
                            self.current_score.score = 0
                            self.safe_frogs = 0
                            self.lives_left = 2
                            self.level = 1
                            self.reset_game()
                            self.respawn()
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
                    self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
                    self.timer_tick(pygame.time.get_ticks() / 1000 - self.start_time)
                    self.collision()
                    self.update_display() 
                    pygame.display.update()
                    self.clock.tick(FPS)
                
                if not self.running and not self.in_start_screen:
                    self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
                    self.timer_tick(pygame.time.get_ticks() / 1000 - self.start_time)                  
                    if 10 - self.current_time > 0:
                        self.respawn_menu.update(str(10 - self.current_time))
                        self.respawn_menu.draw(self.screen)
                    else:
                        self.in_start_screen = True
                    pygame.display.update()
Game().run()