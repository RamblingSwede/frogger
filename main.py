import pygame
import sys 

SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Frogger')
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.frog = pygame.image.load("./resources/frog_placeholder.png").convert_alpha()

    def run(self):
        while True:
            self.screen.fill('Black')
            self.screen.blit(self.frog, (SCREENWIDTH // 2,400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()



            pygame.display.update()

Game().run()