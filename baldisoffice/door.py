import pygame

from settings import *


class Door:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            TILE_SIZE,
            TILE_SIZE
        )

    def draw(self, screen, camera):

        pygame.draw.rect(
            screen,
            (139, 69, 19),
            camera.apply_rect(
                self.rect
            )
        )