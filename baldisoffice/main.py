import pygame
from game import Game
if __name__ == '__main__':
    pygame.init()
    try:
        Game().run()
    finally:
        pygame.quit()
