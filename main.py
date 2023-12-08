import pygame
import sys

SIZE = 32 
SCREENWIDTH, SCREENHEIGHT = SIZE * 40, 720
FPS = 60

class Frog: 
    def __init__(self):
        self.image = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = SCREENWIDTH / 2 
        self.rect.y = SCREENHEIGHT - SIZE 

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger')
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))   
        self.frog = Frog()

    def out_of_bounds(self, dx, dy): 
        x = self.frog.rect.x + dx 
        y = self.frog.rect.y + dy 
        print(y) 
        return x >= SCREENWIDTH or x < 0 or y >= SCREENHEIGHT or y < 0 
        
    def run(self):
        while True:
            self.screen.fill('Black')
            self.screen.blit(self.frog.image, self.frog.rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        if not self.out_of_bounds(-SIZE, 0): 
                            self.frog.rect.x -= SIZE
                    if event.key == pygame.K_d:
                        if not self.out_of_bounds(SIZE, 0): 
                            self.frog.rect.x += SIZE
                    if event.key == pygame.K_w:
                        if not self.out_of_bounds(0, -SIZE): 
                            self.frog.rect.y -= SIZE
                    if event.key == pygame.K_s:
                        if not self.out_of_bounds(0, SIZE): 
                            self.frog.rect.y += SIZE

            pygame.display.update()
            self.clock.tick(60)

Game().run()