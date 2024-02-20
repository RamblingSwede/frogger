import pygame
import threading 

class Floater(pygame.sprite.Sprite): 
    def __init__(self, image, width, x_pos, y_pos, velocity, offset, delay, jump_distance):
        super().__init__()
        self.count = 0 
        self.image = pygame.image.load(image).convert_alpha() 
        self.rect = self.image.get_rect()
        self.width = width 
        self.rect.x = x_pos 
        self.rect.y = y_pos 
        self.velocity = velocity
        self.offset = offset
        self.delay = delay 
        self.jump_distance = jump_distance

    def get_jump_distance(self): 
        return self.jump_distance 

    def update(self, width, group):
        if self.count == self.offset: 
            self.rect.x += self.velocity
            self.count = 0 
            if self.destroy(width): 
                new_floater = self.create_new_floater()
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
    
    

class Log(Floater): 
    def __init__(self, type, size, x_pos):
        if type == 'log_small':
            super().__init__("./resources/floaters/log_2_placeholder.png", 2 * size, 
                             x_pos, size * 5, 1, 3, -2 * size, (size * 1.4, size))

        elif type == 'log_medium':
            super().__init__("./resources/floaters/log_3_placeholder.png", 3 * size, 
                             x_pos, size * 2, 1, 2, -(10 * size), (size * 1.4, size))

        elif type == 'log_large':
            super().__init__("./resources/floaters/log_4_placeholder.png", 4 * size, 
                             x_pos, size * 4, 1, 1, -(10 * size), (size * 1.4, size))

        self.type = type
        self.size = size
            
    def create_new_floater(self): 
        return Log(self.type, self.size, self.delay) 
    
    def get_pos(self):
        return (self.rect.x, self.rect.y)
    

            
class Turtle(Floater): 
    def __init__(self, type, size, width, x_pos):
        if type == 'turtle_medium':
            super().__init__("./resources/floaters/turtle_2_placeholder.png", 2 * size, 
                             x_pos, size * 3, -1, 1, width + 4 * size, (size, size * 1.4))
            self.image_file = "./resources/floaters/turtle_2_placeholder.png"

        elif type == 'turtle_large':
            super().__init__("./resources/floaters/turtle_3_placeholder.png", 3 * size, 
                             x_pos, size * 6, -1, 2, width + 3 * size, (size, size * 1.4))
            self.image_file = "./resources/floaters/turtle_3_placeholder.png"

        self.type = type
        self.size = size
        self.width = width

    def create_new_floater(self):
        return self.generate_turtle()
    

    
class NormalTurtle(Turtle): 
    def __init__(self, type, size, width, x_pos):
            super().__init__(type, size, width, x_pos)

    def generate_turtle(self): 
        return NormalTurtle(self.type, self.size, self.width, self.delay) 


    
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

    def is_diving(self): 
        return self.diving

    def generate_turtle(self): 
        return DivingTurtle(self.type, self.size, self.width, self.delay) 

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