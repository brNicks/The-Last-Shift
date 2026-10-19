import pygame

class NPC:

    def __init__(self, x, y, name, dialogue):

        self.rect = pygame.Rect(x, y, 40, 40)

        self.name = name
        self.dialogue = dialogue

    def draw(self, screen, camera):

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            camera.apply_rect(self.rect)
        )