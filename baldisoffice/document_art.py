"""V62 Parte 19: documentos coletaveis apenas com aparencia nova.
Retangulos e logica de coleta continuam em Game / Item.
"""
from pathlib import Path
import pygame

class DocumentArt:
    def __init__(self):
        folder = Path(__file__).resolve().parent / "assets" / "items"
        self.images = [pygame.image.load(str(folder / f"documento_{i}.png")).convert_alpha()
                       for i in (1, 2, 3)]

    def draw(self, screen, camera, item, index):
        if item.collected:
            return
        target = camera.apply_rect(item.rect) if camera is not None else item.rect
        sprite = self.images[index % len(self.images)]
        screen.blit(sprite, (target.centerx - sprite.get_width() // 2,
                             target.centery - sprite.get_height() // 2))
