import pygame

class CurrentScore:
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
        screen.blit(self.surf, self.rect)

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
        screen.blit(self.surf, self.rect)