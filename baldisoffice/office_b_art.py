"""V62 Parte 20 — arte somente do Escritorio B. Nenhuma hitbox ou regra aqui."""
from pathlib import Path
import pygame

class OfficeBArt:
    def __init__(self):
        folder = Path(__file__).resolve().parent / 'assets' / 'office_b'
        self.image = pygame.image.load(str(folder / 'escritorio_b_polido.png')).convert()
        self.exit_locked = pygame.image.load(str(folder / 'saida_trancada.png')).convert_alpha()
        self.exit_unlocked = pygame.image.load(str(folder / 'saida_liberada.png')).convert_alpha()
        self._shadow = pygame.Surface((1080, 444), pygame.SRCALPHA)

    def draw(self, screen, tension):
        # Preserva o aumento progressivo de escuridao do setor B.
        screen.blit(self.image, (0, 0))
        tick = pygame.time.get_ticks()
        tension = max(0.0, min(100.0, float(tension)))
        # Pequeno escurecimento do piso, mantendo HUD e personagens legiveis.
        opacity = int(max(0, tension - 25) * 0.46)
        if opacity:
            self._shadow.fill((6, 4, 9, min(36, opacity)))
            screen.blit(self._shadow, (100, 174))
        # As quatro luminarias falham em momentos diferentes, como no visual anterior.
        for idx, x in enumerate((309, 559, 809, 1059)):
            cycle = ((tick // 190) + idx * 3) % 19
            fail = (tension >= 25 and cycle in (3, 8)) or (tension >= 60 and cycle in (5, 12, 16)) or (tension >= 85 and cycle in (1, 9, 14))
            color = (37, 34, 36) if fail else (158, 137, 111) if tension >= 60 else (188, 171, 138)
            pygame.draw.rect(screen, color, pygame.Rect(x-54, 106, 109, 4))
        if tension >= 65:
            # Monitor da parede (hotspot de examinacao ja existente) corrompendo.
            phase = (tick // 400) % 7
            if phase in (1, 5):
                pygame.draw.line(screen, (112, 63, 68), (750, 142), (799, 142), 1)
                pygame.draw.line(screen, (110, 87, 83), (758, 149), (795, 149), 1)
        if tension >= 80 and (tick // 100) % 27 == 4:
            # Pulso curto e sutil, sem efeito de tela inteira e sem gameplay.
            flash = pygame.Surface((1080, 444), pygame.SRCALPHA)
            flash.fill((100, 45, 44, 16))
            screen.blit(flash, (100, 174))

    def draw_exit(self, screen, exit_rect, unlocked=False):
        img = self.exit_unlocked if unlocked else self.exit_locked
        screen.blit(img, exit_rect.topleft)
