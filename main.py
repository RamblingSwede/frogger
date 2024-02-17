from Entities.entities import *
from Entities.floaters import * 
from utils import *
from random import randint 
import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 14, SIZE * 15
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
        self.screen             = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) 
        self.background         = Background(SCREENWIDTH, SCREENHEIGHT, SIZE) 
        self.ui                 = UI(SCREENHEIGHT - SIZE)
        self.top_ui             = TopUI()
        self.respawn_menu       = RespawnMenu(SCREENWIDTH, SCREENHEIGHT)
        self.current_score      = Current_Score()
        self.high_score         = Highscore()
        self.splash_screen      = SplashScreen()
        self.in_start_screen    = True 
        self.running            = False
        self.safe_frogs         = 0
        self.lives_left         = 2
        self.floater_group      = pygame.sprite.Group() 
        self.current_floater    = None 
        self.vehicle_group      = pygame.sprite.Group()
        self.final_lilies_group = pygame.sprite.Group() 
        self.frog               = pygame.sprite.GroupSingle()
        self.frog.add(Frog(SCREENWIDTH, SCREENHEIGHT, SIZE)) 
        self.timer              = pygame.USEREVENT + 1
        self.timer_bar          = pygame.sprite.Group()
        pygame.time.set_timer(self.timer, 30000)
        self.movementX          = [False, False]
        self.movementY          = [False, False]
        self.jump_distance      = SIZE 
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.spawn_floaters_lvl_1()
        self.spawn_vehicles_lvl_1() 
        self.spawn_final_lilies()
        self.spawn_timer_bar()

    def spawn_floaters_lvl_1(self): 
        log_small_x = randint(-SIZE * 4, -SIZE * 2)
        log_medium_x = randint(-SIZE * 10, -SIZE * 4)
        log_large_x = randint(-SIZE * 8, -SIZE * 3)
        lily_medium_x = randint(SIZE * 9, SCREENWIDTH + SIZE * 4)
        lily_large_x = randint(SIZE * 6, SCREENWIDTH + SIZE * 2)
        self.floater_group.add(Log('log_small', SIZE, log_small_x))
        self.floater_group.add(Log('log_small', SIZE, log_small_x - SCREENWIDTH / 3 - SIZE))
        self.floater_group.add(Log('log_small', SIZE, log_small_x - 2 * SCREENWIDTH / 3 - SIZE))
        self.floater_group.add(Log('log_medium', SIZE, log_medium_x))
        self.floater_group.add(Log('log_medium', SIZE, log_medium_x - SIZE * 6))
        self.floater_group.add(Log('log_medium', SIZE, log_medium_x - SIZE * 11))
        self.floater_group.add(Log('log_medium', SIZE, log_medium_x - SIZE * 16))
        self.floater_group.add(Log('log_large', SIZE, log_large_x))
        self.floater_group.add(Log('log_large', SIZE, log_large_x - SIZE * 8))
        self.floater_group.add(Log('log_large', SIZE, log_large_x - SIZE * 16))
        self.floater_group.add(Lily('lily_medium', SIZE, SCREENWIDTH, lily_medium_x))
        self.floater_group.add(Lily('lily_medium', SIZE, SCREENWIDTH, lily_medium_x + SIZE * 5))
        self.floater_group.add(Lily('lily_medium', SIZE, SCREENWIDTH, lily_medium_x + SIZE * 10))
        self.floater_group.add(Lily('lily_medium', SIZE, SCREENWIDTH, lily_medium_x + SIZE * 15))
        self.floater_group.add(Lily('lily_large', SIZE, SCREENWIDTH, lily_large_x))
        self.floater_group.add(Lily('lily_large', SIZE, SCREENWIDTH, lily_large_x + SIZE * 5))
        self.floater_group.add(Lily('lily_large', SIZE, SCREENWIDTH, lily_large_x + SIZE * 10))
        self.floater_group.add(Lily('lily_large', SIZE, SCREENWIDTH, lily_large_x + SIZE * 15))

    def spawn_vehicles_lvl_1(self): 
        car_x = randint(SIZE * 2, SIZE * 8)
        tractor_x = randint(SIZE * 2, SIZE * 8)
        truck_x = randint(SIZE * 6, SIZE * 10)
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x))
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 5))
        self.vehicle_group.add(Vehicle('car', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 10))
        self.vehicle_group.add(Vehicle('tractor', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x))
        self.vehicle_group.add(Vehicle('tractor', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x - SIZE * 4))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x + SIZE * 6))
        self.vehicle_group.add(Vehicle('truck', SCREENWIDTH, SCREENHEIGHT, SIZE, truck_x + SIZE * 10))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x  - SIZE * 5))
        self.vehicle_group.add(Vehicle('car2', SCREENWIDTH, SCREENHEIGHT, SIZE, tractor_x  - SIZE * 10))
        self.vehicle_group.add(Vehicle('tractor2', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x))
        self.vehicle_group.add(Vehicle('tractor2', SCREENWIDTH, SCREENHEIGHT, SIZE, car_x + SIZE * 4))

    def spawn_final_lilies(self): 
        y = SIZE + SIZE / 4 + 2 
        for i in range(5): 
            x = 16 + 6 + i * SIZE * 3 
            self.final_lilies_group.add(Final_Lily(x, y))

    def spawn_timer_bar(self):
        for i in range(0, 30):
            offset = i * 10
            self.timer_bar.add(Timer_Bar(SCREENHEIGHT, SIZE, offset))

    def timer_tick(self):
        for bar in self.timer_bar:
            offset = (39 - self.current_time) * 10
            bar.destroy(offset)

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
                    if platform.within_bounds(self.frog.sprite.rect.x, SIZE): 
                        self.set_jump_distance(platform) 
                        self.frog.sprite.match_speed(platform.offset, platform.velocity)
                        if platform != self.current_floater: 
                            print('another platform')
                            self.current_floater = platform
                            break 
                    else:
                        self.lose_life() 
            else:
                self.lose_life() 
        else: 
            self.jump_distance = SIZE 
            self.current_floater = None 

    def handle_final_platform_hit(self): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.final_lilies_group, False): 
            lily = pygame.sprite.spritecollide(self.frog.sprite, self.final_lilies_group, False)[0] 
            if lily.hit(self.frog.sprite.get_x(), SIZE): 
                lily.set_occupied() 
                if self.safe_frogs == 4:
                    self.level_completed()
                else:
                    self.current_score.visited_pos.clear()
                    self.safe_frogs += 1
                    self.current_score.update_score('frogsaved',  30 - self.current_time)
                    print('Frog made it to safety')
                    self.respawn()
            else: 
                print('Didn\'t hit')
                self.lose_life() 
        elif self.frog.sprite.rect.y == SIZE:
            self.lose_life() 

    def set_jump_distance(self, platform): 
        dists = platform.get_jump_distance() 
        if self.movementX[0]: 
            self.jump_distance = dists[0] 
        elif self.movementX[1]: 
            self.jump_distance = dists[1] 


    def in_river(self): 
        return self.frog.sprite.rect.y < SIZE * 7 and self.frog.sprite.rect.y > SIZE

    def lose_life(self): 
        if self.movementY[1]:
            self.current_score.score -= 10
            self.current_score.visited_pos.pop()
        if self.lives_left > 0:
            self.lives_left -= 1
            self.respawn()
        else:
            self.running = False

    def respawn(self):
        pygame.time.set_timer(self.timer, 30000)
        self.start_time = int(pygame.time.get_ticks() / 1000)
        for bar in self.timer_bar:
            bar.kill()
        self.frog.sprite.rect.x = SCREENWIDTH / 2
        self.frog.sprite.rect.y = SCREENHEIGHT - SIZE * 2
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
        for lily in self.final_lilies_group:
            lily.kill()
        for bar in self.timer_bar:
            bar.kill()
        self.spawn_vehicles_lvl_1()
        self.spawn_floaters_lvl_1()
        self.spawn_final_lilies()
        self.spawn_timer_bar()

    def level_completed(self):
        print('Level completed')
        self.current_score.update_score('frogsaved',  30 - self.current_time)
        self.current_score.update_score('levelcomplete',  30 - self.current_time)
        if int(self.current_score.score) > int(self.high_score.score):
            self.high_score.update(self.current_score.score)
        self.high_score.refresh()
        self.level += 1
        self.safe_frogs = 0
        self.reset_game()
        self.respawn()
                    
    # Frog must be added last so that it is the most forward object on the display 
    def update_display(self): 
        self.screen.fill('Black')
        self.background.draw(self.screen) 
        self.vehicle_group.update(SCREENWIDTH, SCREENHEIGHT, SIZE, self.vehicle_group)
        self.vehicle_group.draw(self.screen)
        self.floater_group.update(SCREENWIDTH, self.floater_group)
        self.floater_group.draw(self.screen)
        self.final_lilies_group.draw(self.screen) 
        self.frog.update(SCREENWIDTH, SCREENHEIGHT, SIZE, self.jump_distance, self.movementX, self.movementY)
        self.frog.draw(self.screen)
        self.ui.draw(self.screen)
        self.timer_bar.draw(self.screen)
        self.top_ui.draw(self.screen)
        self.current_score.draw(self.screen, self.current_score.score)
        self.high_score.draw(self.screen)

    def start_screen(self):
        self.screen.fill('Black')
        self.background.draw(self.screen)
        self.final_lilies_group.draw(self.screen) 
        self.top_ui.draw(self.screen)
        self.current_score.draw(self.screen, self.current_score.score)
        self.high_score.draw(self.screen)
        self.splash_screen.draw(self.screen)
        pygame.display.update() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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
                        self.current_score.score = 0
                        self.safe_frogs = 0
                        self.lives_left = 2
                        self.level = 1
                        self.reset_game()
                        self.respawn()
                    if event.type == pygame.MOUSEBUTTONDOWN and not self.running and mx >= 235 and mx <= 300 and my >= 264 and my <= 294:
                        self.in_start_screen = True
                    if event.type == pygame.QUIT:
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
                                self.current_score.update_score('stepforward', 30 - self.current_time)
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
                    self.timer_tick()
                    self.collision()
                    self.update_display() 
                    pygame.display.update()
                    self.clock.tick(FPS)
                
                if not self.running and not self.in_start_screen:
                    self.current_time = int(pygame.time.get_ticks() / 1000) - self.start_time
                    if 10 - self.current_time > 0:
                        self.respawn_menu.update(str(10 - self.current_time))
                        self.respawn_menu.draw(self.screen)
                    else:
                        self.in_start_screen = True
                    pygame.display.update()
Game().run()