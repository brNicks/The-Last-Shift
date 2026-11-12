import pygame
from sprite_loader import load_sprite, draw_character

class NPC:

    def __init__(self, x, y, name, dialogue):

        self.rect = pygame.Rect(x, y, 40, 40)

        self.name = name
        self.dialogue = dialogue
        # Clara é recepcionista: permanece parada, sem animações de caminhada.
        self.sprite = load_sprite("clara/seated.png")

    def draw(self, screen, camera):

        if not draw_character(screen, self.sprite, self.rect, camera, (58, 78)):
            pygame.draw.rect(screen, (255, 255, 0), camera.apply_rect(self.rect))