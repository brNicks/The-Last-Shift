"""Polimento gráfico da recepção — The Last Shift V62 / Parte 15.

Renderização somente visual: não altera retângulos, eventos ou colisões.
Coordenadas em pixels do mundo, acompanhando a câmera existente.
"""
from pathlib import Path
import pygame

class ReceptionArt:
    def __init__(self):
        filename = (Path(__file__).resolve().parent / "assets" / "scenario"
                    / "recepcao_piso_paredes_v62_p15.png")
        self.background = pygame.image.load(str(filename)).convert()

    @staticmethod
    def _at(camera, rect):
        return camera.apply_rect(pygame.Rect(rect))

    def draw_background(self, screen, camera):
        screen.blit(self.background, (-camera.offset_x, -camera.offset_y))

    def draw_door(self, screen, camera, door_rect, active, letter):
        """Reveste a mesma posição da porta sem mudar seu retângulo de colisão."""
        rect = self._at(camera, door_rect)
        # sombra externa e portal metálico
        pygame.draw.rect(screen, (23, 26, 28), rect.move(4, 4))
        pygame.draw.rect(screen, (27, 32, 35), rect)
        pygame.draw.rect(screen, (121, 116, 102), rect, 3)
        interior = rect.inflate(-10,-8)
        pygame.draw.rect(screen, (57, 51, 45) if active else (44, 45, 46), interior)
        pygame.draw.rect(screen, (37, 48, 50) if active else (35, 38, 39),
                         (interior.x+6, interior.y+5, max(4,interior.width-12),
                          max(4,interior.height-26)))
        pygame.draw.rect(screen, (73, 88, 89) if active else (55, 59, 59),
                         (interior.x+9, interior.y+8, 4, max(3,interior.height-36)))
        pygame.draw.line(screen, (151, 138, 112), (rect.x+6, rect.bottom-9),
                         (rect.right-6, rect.bottom-9), 2)
        pygame.draw.rect(screen, (181, 174, 151),
                         (rect.right-17, rect.centery+6, 5, 3))
        if not active:
            pygame.draw.rect(screen, (127, 73, 66), (rect.centerx-5, rect.centery+5, 11, 10))
            pygame.draw.rect(screen, (49, 46, 44), (rect.centerx-4, rect.centery, 9, 7), 2)

    def draw_badge(self, screen, camera, badge):
        if badge.collected:
            return
        rect = self._at(camera, badge.rect)
        pygame.draw.rect(screen, (23, 26, 26), rect.move(3, 3))
        pygame.draw.rect(screen, (209, 204, 185), rect.inflate(-2, -1), border_radius=2)
        pygame.draw.rect(screen, (104, 55, 50),
                         (rect.x+5, rect.y+2, rect.width-10, 5))
        pygame.draw.rect(screen, (63, 65, 67), (rect.x+6, rect.y+11, 8, 9))
        pygame.draw.line(screen, (94, 93, 85), (rect.x+17,rect.y+13),
                         (rect.x+rect.width-5,rect.y+13), 2)
        pygame.draw.line(screen, (109, 108, 99), (rect.x+17,rect.y+19),
                         (rect.x+rect.width-6,rect.y+19), 2)
