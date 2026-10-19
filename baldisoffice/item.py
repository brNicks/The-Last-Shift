import pygame

class Item:

    def __init__(self, x, y, name):

        self.rect = pygame.Rect(
            x,
            y,
            30,
            30
        )

        self.name = name

        self.collected = False

    def draw(self, screen, camera):

        if self.collected:
            return

        pygame.draw.rect(
            screen,
            (0,255,255),
            camera.apply_rect(self.rect)
        )