import pygame
import threading 

class Floater(pygame.sprite.Sprite): 
    def __init__(self, image, width, x_pos, y_pos, velocity, offset, spawn_delay, jump_distance):
        super().__init__()
        self.count = 0 
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
        self.width = width 
        self.rect.x = x_pos 
        self.rect.y = y_pos 
        self.velocity = velocity
        self.offset = offset
        self.spawn_delay = spawn_delay 
        self.jump_distance = jump_distance

    def get_jump_distance(self): 
        return self.jump_distance 
    
    def get_pos(self):
        return (self.rect.x, self.rect.y)

    def update(self, width, group, friend_frog):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.count = 0 
            if self.destroy(width): 
                new_floater = self.create_new_floater(friend_frog)
                group.add(new_floater)
        self.count += 1 

    def destroy(self, width):
        if self.velocity > 0: 
            if self.rect.x >= width: 
                self.kill()
                return True 
            return False
        else: 
            if self.rect.x <= -self.width: 
                self.kill() 
                return True
            return False 
        
    def within_bounds(self, x_left, size): 
        x_right = x_left + size 
        margin = size * (4 / 10)
        return x_left > self.rect.x - margin and x_right < self.rect.x + self.width + margin 
    
    def hostile(self, frog): 
        return False
    

class Crocodile(Floater):
    def __init__(self, size, x_pos):
        super().__init__("./resources/floaters/crocodile.png", 3 * size, 
                             x_pos, size * 2, 1, 2, -(10 * size), (size * 1.4, size))
        self.size = size
        self.croc_image_file = "./resources/floaters/crocodile.png"
        self.croc_image_file_mouth_open = "./resources/floaters/crocodile_mouth_open.png"
        self.mouth_open = False 
        self.timer = threading.Timer(1.2, self.update_crocodile)
        self.timer.start()

    def update_crocodile(self):
        if self.mouth_open:
            self.image = pygame.image.load(self.croc_image_file).convert_alpha() 
        else:
            self.image = pygame.image.load(self.croc_image_file_mouth_open).convert_alpha()
        self.mouth_open = not self.mouth_open
        self.timer = threading.Timer(1.2, self.update_crocodile)
        self.timer.start()
        
    def create_new_floater(self, friend_frog):
        return Crocodile(self.size, self.spawn_delay)
    
    def hostile(self, frog):
        return True
    
    

class Log(Floater): 
    def __init__(self, type, size, x_pos, lvl=1):
        self.level = lvl
        if type == 'log_small':
            super().__init__("./resources/floaters/log_small.png", 2 * size, 
                             x_pos, size * 5, 1, 3, -2 * size, (size * 1.4, size))

        elif type == 'log_medium':
            offset = 1
            if lvl == 1 or lvl == 2:
                offset = 2
            super().__init__("./resources/floaters/log_medium.png", 3 * size, 
                             x_pos, size * 2, 1, offset, -(10 * size), (size * 1.4, size))

        elif type == 'log_large':
            offset = 2
            if lvl == 1:
                offset = 1
            super().__init__("./resources/floaters/log_large.png", 4 * size, 
                             x_pos, size * 4, 1, offset, -(10 * size), (size * 1.4, size))

        self.type = type
        self.size = size
            
    def create_new_floater(self, friend_frog): 
        log = Log(self.type, self.size, self.spawn_delay, self.level)
        if (friend_frog.sprite.out_of_bounds() and self.type == 'log_small'):
            friend_frog.sprite.reset(log)
        return log
    


class SnakeLog(Floater):
    def __init__(self, size, x_pos):
        super().__init__("./resources/floaters/log_large.png", 4 * size, 
                             x_pos, size * 4, 1, 2, -(10 * size), (size * 1.4, size))
        self.size = size 
        self.init_snake()

    def init_snake(self):
        self.snake = self.Snake(self, self.width)

    def update(self, width, group, friend_frog):
        super().update(width, group, friend_frog)
        self.snake.update()

    def draw(self, screen):
        self.snake.draw(screen)

    def create_new_floater(self, friend_frog):
        return SnakeLog(self.size, self.spawn_delay)
    
    def hostile(self, frog): 
        return pygame.sprite.collide_rect(frog, self.snake)
    
    class Snake(pygame.sprite.Sprite):
        def __init__(self, log, width):
            super().__init__()
            self.log = log
            self.count = 0 
            self.image = pygame.image.load("./resources/floaters/snake_placeholder.png").convert_alpha() 
            self.rect = self.image.get_rect()
            self.width = 32 
            self.log_width = width
            self.rect.x = log.get_pos()[0]
            self.rect.y = log.get_pos()[1]
            self.velocity = log.velocity
            self.offset = 2
            self.x = 0
            self.right = True

        def update(self):
            log_x = self.log.get_pos()[0]
            self.rect.x = log_x + self.x
            if self.count == self.offset: 
                if self.right:
                    self.x += self.velocity
                else:
                    self.x -= self.velocity
                self.count = 0 
                if self.rect.x >= log_x + self.log.width - self.width:
                    self.right = False
                    self.offset = 2
                if self.rect.x <= log_x:
                    self.right = True
                    self.offset = 1
            self.count += 1 

        def draw(self, screen):
            screen.blit(self.image, self.rect)
    


class Turtle(Floater): 
    def __init__(self, type, size, width, x_pos):
        if type == 'turtle_medium':
            super().__init__("./resources/floaters/turtle_small.png", 2 * size, 
                             x_pos, size * 3, -1, 1, width, (size, size * 1.4))
            self.image_file = "./resources/floaters/turtle_small.png"

        elif type == 'turtle_large':
            super().__init__("./resources/floaters/turtle_medium.png", 3 * size, 
                             x_pos, size * 6, -1, 2, width + size, (size, size * 1.4))
            self.image_file = "./resources/floaters/turtle_medium.png"

        self.type = type
        self.size = size
        self.width = width

    def create_new_floater(self, friend_frog):
        return self.generate_turtle()
    

    
class NormalTurtle(Turtle): 
    def __init__(self, type, size, width, x_pos):
            super().__init__(type, size, width, x_pos)

    def generate_turtle(self): 
        return NormalTurtle(self.type, self.size, self.width, self.spawn_delay) 


    
class DivingTurtle(Turtle): 
    def __init__(self, type, size, width, x_pos):
        if type == 'turtle_medium':
            super().__init__(type, size, width, x_pos)
            self.diving_image_file1 = "./resources/floaters/1diving_turtle_2_placeholder.png"
            self.diving_image_file2 = "./resources/floaters/2diving_turtle_2_placeholder.png"
            self.diving_image_file3 = "./resources/floaters/diving_turtle_2_placeholder.png"

        elif type == 'turtle_large':
            super().__init__(type, size, width, x_pos)
            self.diving_image_file1 = "./resources/floaters/1diving_turtle_3_placeholder.png"
            self.diving_image_file2 = "./resources/floaters/2diving_turtle_3_placeholder.png"
            self.diving_image_file3 = "./resources/floaters/diving_turtle_3_placeholder.png"

        self.timer_count = 0
        self.diving = False 
        self.timer = threading.Timer(0.8, self.update_turtle)
        self.timer.start()

    def hostile(self, frog):
        return self.is_diving()

    def is_diving(self): 
        return self.diving

    def generate_turtle(self): 
        return DivingTurtle(self.type, self.size, self.width, self.spawn_delay) 

    def update_turtle(self): 
        self.timer_count += 1
        x = self.rect.x
        y = self.rect.y
        if self.timer_count % 5 == 0: 
            self.diving = False 
            self.image = pygame.image.load(self.image_file).convert_alpha()
            self.timer = threading.Timer(0.8, self.update_turtle)
        
        elif self.timer_count % 5 == 1: 
            self.timer = threading.Timer(0.8, self.update_turtle)

        elif self.timer_count % 5 == 2: 
            self.image = pygame.image.load(self.diving_image_file1).convert_alpha()
            self.timer = threading.Timer(0.8, self.update_turtle)

        elif self.timer_count % 5 == 3: 
            self.image = pygame.image.load(self.diving_image_file2).convert_alpha()
            self.timer = threading.Timer(0.8, self.update_turtle)

        elif self.timer_count % 5 == 4: 
            self.image = pygame.image.load(self.diving_image_file3).convert_alpha()
            self.timer = threading.Timer(0.8, self.update_turtle)
            self.diving = True

        else: 
            return

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer.start()