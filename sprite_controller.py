import pygame
from sprite_generator import *

class SpriteController:
    def __init__(self, screen_width, screen_height, block_size, river_y):
        self.floater_group      = pygame.sprite.Group()
        self.vehicle_group      = pygame.sprite.Group()
        self.sprite_generator   = spriteGenerator(block_size, screen_width, screen_height)
        self.lilies_group       = pygame.sprite.Group()
        self.frog               = pygame.sprite.GroupSingle()
        self.frog.add(NormalFrog(screen_width, screen_height, block_size))
        self.friend_frog        = pygame.sprite.GroupSingle()
        self.block_size         = block_size
        self.river_y            = river_y

    def handle_collisions(self, game):
        self.handle_vehicle_hit(game) 
        self.handle_floater_hit(game) 
        self.handle_final_platform_hit(game) 

    def handle_vehicle_hit(self, game): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.vehicle_group, False):
            game.lose_life() 

    def handle_floater_hit(self, game): 
        if self.in_river():
            if pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False):
                platforms = pygame.sprite.spritecollide(self.frog.sprite, self.floater_group, False)
                for platform in platforms:
                    if platform.within_bounds(self.frog.sprite.rect.x, self.block_size): 
                        if platform.hostile(self.frog.sprite):
                            game.lose_life()
                            break
                        game.set_jump_distance(platform) 
                        self.frog.sprite.match_speed(platform.offset, platform.velocity)
                        self.handle_friend_frog_hit()
                    else:
                        game.lose_life() 
            else:
                game.lose_life() 
        else: 
            game.jump_distance = self.block_size 

    def handle_friend_frog_hit(self):
        if self.frog.sprite.carrying_friend() or self.friend_frog.sprite.is_safe():
            return
        try: 
            if self.friend_frog.sprite.hit():
                self.frog.sprite.set_carry_friend(True)
                self.friend_frog.sprite.set_carried()
        except Exception as e: 
            print("Friend frog is no more: ", e)

    def handle_final_platform_hit(self, game): 
        if pygame.sprite.spritecollide(self.frog.sprite, self.lilies_group, False): 
            lily = pygame.sprite.spritecollide(self.frog.sprite, self.lilies_group, False)[0] 
            if lily.hit(self.frog.sprite.get_x(), self.block_size): 
                lily.set_occupied() 
                game.handle_reached_final_lily(lily, self.frog, self.friend_frog)
            else: 
                game.lose_life() 
        elif self.frog.sprite.rect.y == self.block_size:
            game.lose_life() 

    def in_river(self): 
        return self.frog.sprite.rect.y > self.river_y[0] and self.frog.sprite.rect.y < self.river_y[1]