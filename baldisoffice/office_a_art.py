"""Parte 18 - somente a aparencia do Escritorio A; nenhuma hitbox aqui."""
from pathlib import Path
import pygame

class OfficeAArt:
    def __init__(self):
        image_path = Path(__file__).resolve().parent / "assets" / "office_a" / "escritorio_a_polido.png"
        self.image = pygame.image.load(str(image_path)).convert()
        folder = image_path.parent
        self.exit_locked = pygame.image.load(str(folder / "saida_trancada.png")).convert_alpha()
        self.exit_unlocked = pygame.image.load(str(folder / "saida_liberada.png")).convert_alpha()

    def draw(self, screen):
        screen.blit(self.image, (0, 0))

    def draw_exit(self, screen, exit_rect, unlocked=False):
        """Mesmo retângulo de saída do jogo: muda SOMENTE a arte."""
        image = self.exit_unlocked if unlocked else self.exit_locked
        screen.blit(image, exit_rect.topleft)
