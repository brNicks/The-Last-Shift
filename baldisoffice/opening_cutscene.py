"""V62 Parte 22.1 - chegada de onibus, desembarque e portas realmente abrindo.

Cena isolada do gameplay e sem alterar o spawn ou flags da Fase 1.
ESC/Espaco continuam pulando a cinematica.
"""
from pathlib import Path
import math
import pygame
from settings import WIDTH, HEIGHT


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def smooth(v):
    v = clamp(v)
    return v * v * (3.0 - 2.0 * v)


def mix(a, b, t):
    return a + (b - a) * t


class OpeningCutscene:
    DURATION = 15.50
    # Cronograma unico; a abertura nao depende de eventos do gameplay.
    BUS_ARRIVE_END = 0.90
    BUS_DOOR_START = 1.05
    BUS_DOOR_OPEN_END = 1.55
    DISEMBARK_START = 1.62
    DISEMBARK_END = 2.72
    BUS_DOOR_CLOSE_START = 2.80
    BUS_DOOR_CLOSE_END = 3.30
    BUS_DEPART_START = 3.35
    BUS_DEPART_END = 4.95
    HERO_WALK_START = 3.75
    HERO_WALK_END = 8.35
    BUILDING_DOOR_START = 8.18
    BUILDING_DOOR_OPEN_END = 8.98
    HERO_ENTER_START = 8.98
    HERO_ENTER_END = 10.06
    CAMERA_RISE_START = 10.12
    CAMERA_RISE_END = 12.22
    INSIDE_START = 12.48

    BUS_POS = (24, 458)
    BUS_SIZE = (610, 205)
    BUS_DOOR = pygame.Rect(64, 55, 64, 124)
    BUILDING_BAY = pygame.Rect(661, 440, 178, 155)

    def __init__(self, asset_dir):
        assets = Path(asset_dir)
        self.outside = pygame.image.load(str(assets / 'cutscenes/fachada_the_last_shift.png')).convert()
        self.lobby = pygame.image.load(str(assets / 'scenario/recepcao_piso_paredes_v62_p15.png')).convert()
        bus_png = pygame.image.load(str(assets / 'cutscenes/onibus_linha04.png')).convert_alpha()
        self.bus = pygame.transform.smoothscale(bus_png, self.BUS_SIZE)
        self.bus_left_pane = self.bus.subsurface(pygame.Rect(64, 55, 32, 124)).copy()
        self.bus_right_pane = self.bus.subsurface(pygame.Rect(96, 55, 32, 124)).copy()
        bay = self.BUILDING_BAY
        # As folhas mantem os detalhes da arte original, mas deslizam de verdade.
        src_y = self.outside.get_height() - HEIGHT + bay.top
        self.entrance_left = self.outside.subsurface((bay.x, src_y, bay.w // 2, bay.h)).copy()
        self.entrance_right = self.outside.subsurface((bay.x + bay.w // 2, src_y, bay.w - bay.w // 2, bay.h)).copy()
        self.hero = {}
        for direction in ('direita', 'cima', 'baixo'):
            root = assets / 'sprites/v62_neutro/protagonista' / direction
            self.hero[direction] = [
                pygame.image.load(str(root / f'{idx}.png')).convert_alpha()
                for idx in range(4)
            ]
        self.elapsed = 0.0
        self.caption = pygame.font.SysFont('consolas', 25, bold=True)
        self.tiny = pygame.font.SysFont('consolas', 18)

    def reset(self):
        self.elapsed = 0.0

    def update(self, dt):
        self.elapsed += min(0.10, max(0.0, dt))
        return self.elapsed >= self.DURATION

    @staticmethod
    def _alpha_cover(screen, alpha):
        if alpha <= 0:
            return
        layer = pygame.Surface((WIDTH, HEIGHT))
        layer.fill((7, 10, 15))
        layer.set_alpha(round(clamp(alpha) * 255))
        screen.blit(layer, (0, 0))

    def _hero(self, screen, x, foot_y, direction, moving, scale=1.0, opacity=255, clip=None):
        if opacity <= 0:
            return
        idx = (int(self.elapsed / 0.145) % 4) if moving else 1
        sprite = self.hero[direction][idx]
        w = max(10, round(90 * scale))
        h = max(14, round(110 * scale))
        sprite = pygame.transform.scale(sprite, (w, h))
        if opacity < 255:
            sprite.set_alpha(round(clamp(opacity / 255.0) * 255))
        original_clip = screen.get_clip()
        if clip is not None:
            screen.set_clip(original_clip.clip(clip))
        shadow = pygame.Surface((max(10, int(w * .49)), 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (7, 12, 19, int(85 * scale)), shadow.get_rect())
        screen.blit(shadow, (int(x - shadow.get_width() / 2), int(foot_y - 4)))
        screen.blit(sprite, (int(x - w / 2), int(foot_y - h)))
        if clip is not None:
            screen.set_clip(original_clip)

    @classmethod
    def bus_state(cls, t):
        """Retorna posicao, abertura da porta e estado para testes de cronologia."""
        if t < cls.BUS_ARRIVE_END:
            x = mix(240, cls.BUS_POS[0], smooth(t / cls.BUS_ARRIVE_END))
        elif t < cls.BUS_DEPART_START:
            x = cls.BUS_POS[0]
        else:
            x = mix(cls.BUS_POS[0], -660,
                    smooth((t - cls.BUS_DEPART_START) /
                           (cls.BUS_DEPART_END - cls.BUS_DEPART_START)))
        if t < cls.BUS_DOOR_START:
            opened = 0.0
        elif t < cls.BUS_DOOR_OPEN_END:
            opened = smooth((t - cls.BUS_DOOR_START) / (cls.BUS_DOOR_OPEN_END - cls.BUS_DOOR_START))
        elif t < cls.BUS_DOOR_CLOSE_START:
            opened = 1.0
        else:
            opened = 1.0 - smooth((t - cls.BUS_DOOR_CLOSE_START) /
                                   (cls.BUS_DOOR_CLOSE_END - cls.BUS_DOOR_CLOSE_START))
        return x, clamp(opened)

    @classmethod
    def exterior_door_state(cls, t):
        # As portas abrem ANTES da travessia. Nao atravessa porta fechada.
        if t < cls.BUILDING_DOOR_START:
            return 0.0
        if t < cls.BUILDING_DOOR_OPEN_END:
            return smooth((t - cls.BUILDING_DOOR_START) /
                          (cls.BUILDING_DOOR_OPEN_END - cls.BUILDING_DOOR_START))
        if t <= cls.HERO_ENTER_END:
            return 1.0
        return 1.0 - smooth((t - cls.HERO_ENTER_END) / 0.65)

    def _draw_bus(self, screen, x, door_open):
        x, y = int(x), self.BUS_POS[1]
        screen.blit(self.bus, (x, y))
        if door_open <= 0:
            return
        # Substitui a area das folhas fechadas por um vao escuro.
        # As folhas usam recortes da arte original e sao recortadas pelo portal.
        door = self.BUS_DOOR
        canvas = pygame.Surface((door.w, door.h), pygame.SRCALPHA)
        canvas.fill((12, 25, 32, 245))
        pygame.draw.rect(canvas, (67, 91, 95), (5, 2, door.w - 10, door.h - 5), 2)
        pygame.draw.line(canvas, (203, 177, 104), (10, 18), (10, door.h - 6), 3)
        pygame.draw.line(canvas, (203, 177, 104), (door.w - 11, 18), (door.w - 11, door.h - 6), 3)
        pygame.draw.line(canvas, (69, 87, 88), (5, door.h - 8), (door.w - 6, door.h - 8), 5)
        step = round((door.w // 2) * door_open)
        canvas.blit(self.bus_left_pane, (-step, 0))
        canvas.blit(self.bus_right_pane, (door.w // 2 + step, 0))
        screen.blit(canvas, (x + door.left, y + door.top))

    def _draw_entrance(self, screen, opening):
        if opening <= 0:
            return
        rect = self.BUILDING_BAY
        portal = pygame.Surface(rect.size, pygame.SRCALPHA)
        # Sala interna perceptivel: profundidade, iluminacao e piso.
        portal.fill((13, 27, 34, 255))
        pygame.draw.rect(portal, (38, 66, 71), (9, 6, rect.w - 18, rect.h - 8))
        pygame.draw.polygon(portal, (29, 48, 52),
                            [(8, 6), (42, 20), (42, 123), (8, 153)])
        pygame.draw.polygon(portal, (31, 51, 55),
                            [(rect.w - 8, 6), (rect.w - 42, 20),
                             (rect.w - 42, 123), (rect.w - 8, 153)])
        pygame.draw.polygon(portal, (68, 95, 91),
                            [(43, 128), (rect.w - 43, 128),
                             (rect.w - 11, 154), (11, 154)])
        for i in range(3):
            x1 = rect.w // 2
            pygame.draw.line(portal, (94, 125, 115),
                             (x1, 128 + i * 8), (x1, 140 + i * 5), 1)
        for yy, half_width in ((18, 28), (36, 23), (57, 16)):
            pygame.draw.rect(portal, (128, 177, 168),
                             (rect.w // 2 - half_width, yy, half_width * 2, 3))
        move = round(rect.w / 2 * clamp(opening))
        portal.blit(self.entrance_left, (-move, 0))
        portal.blit(self.entrance_right, (rect.w // 2 + move, 0))
        # A moldura fica fixa, mesmo quando o vidro desliza.
        pygame.draw.rect(portal, (21, 33, 40), portal.get_rect(), 4)
        pygame.draw.line(portal, (86, 111, 108), (5, 5), (rect.w - 5, 5), 2)
        screen.blit(portal, rect.topleft)

    def _exterior(self, screen, t):
        camera_bottom = self.outside.get_height() - HEIGHT
        offset = camera_bottom
        if t >= self.CAMERA_RISE_START:
            offset = int(mix(camera_bottom, 10,
                             smooth((t - self.CAMERA_RISE_START) /
                                    (self.CAMERA_RISE_END - self.CAMERA_RISE_START))))
        screen.blit(self.outside, (0, -offset))
        if t < self.CAMERA_RISE_START:
            shade = pygame.Surface((WIDTH, 170), pygame.SRCALPHA)
            shade.fill((6, 9, 14, 25))
            screen.blit(shade, (0, HEIGHT - 170))
            # A porta da fachada abre na frente da caminhada de entrada.
            self._draw_entrance(screen, self.exterior_door_state(t))
            bx, bus_open = self.bus_state(t)
            if t <= self.BUS_DEPART_END:
                self._draw_bus(screen, bx, bus_open)

            if self.DISEMBARK_START <= t < self.DISEMBARK_END:
                k = smooth((t - self.DISEMBARK_START) /
                           (self.DISEMBARK_END - self.DISEMBARK_START))
                x = mix(112, 173, k)
                foot = mix(601, 643, k)
                # Primeiro aparece pela abertura; depois pisa na calcada.
                clip = None
                if k < 0.36:
                    clip = pygame.Rect(int(bx) + self.BUS_DOOR.x,
                                       self.BUS_POS[1] + self.BUS_DOOR.y,
                                       self.BUS_DOOR.w, self.BUS_DOOR.h)
                self._hero(screen, x, foot, 'direita', True, .82, clip=clip)
            elif self.DISEMBARK_END <= t < self.HERO_WALK_START:
                self._hero(screen, 173, 643, 'direita', False, .86)
            elif self.HERO_WALK_START <= t < self.HERO_WALK_END:
                k = smooth((t - self.HERO_WALK_START) /
                           (self.HERO_WALK_END - self.HERO_WALK_START))
                self._hero(screen, mix(173, 752, k), mix(643, 616, k),
                           'direita', True, .86)
            elif self.HERO_WALK_END <= t < self.HERO_ENTER_START:
                self._hero(screen, 752, 616, 'cima', False, .86)
            elif self.HERO_ENTER_START <= t <= self.HERO_ENTER_END:
                k = smooth((t - self.HERO_ENTER_START) /
                           (self.HERO_ENTER_END - self.HERO_ENTER_START))
                self._hero(screen, 752, mix(616, 558, k), 'cima', True,
                           mix(.86, .62, k),
                           round(255 * (1.0 - smooth((k - .78) / .22))))
            if t < 3.70:
                label = '06:47  /  CHEGADA AO PONTO'
            elif t < 8.35:
                label = 'PRIMEIRO TURNO  /  THE LAST SHIFT'
            else:
                label = 'SEDE DA THE LAST SHIFT'
        else:
            label = 'UM PREDIO GRANDE DEMAIS PARA UM TURNO...'
        text = self.caption.render(label, True, (232, 232, 227))
        screen.blit(text, (37, 35))
        if self.INSIDE_START - .60 < t < self.INSIDE_START:
            self._alpha_cover(screen, smooth((t - (self.INSIDE_START - .60)) / .60))

    def _inside(self, screen, t):
        screen.fill((17, 19, 22))
        progress = clamp((t - self.INSIDE_START) / 2.40)
        base = pygame.transform.scale(self.lobby, (1500, 720))
        screen.blit(base, (int(mix(-86, -25, smooth(progress))), 0))
        # Hall de entrada em primeiro plano.
        portal = pygame.Rect(640, 458, 247, 262)
        pygame.draw.rect(screen, (17, 27, 32), portal)
        pygame.draw.rect(screen, (36, 63, 69), (650, 470, 226, 238))
        pygame.draw.rect(screen, (108, 127, 124), (655, 490, 215, 4))
        # As portas ja estao abertas quando ele aparece do outro lado.
        if t < 14.75:
            slide = 1.0
        else:
            slide = 1.0 - smooth((t - 14.75) / .48)
        leaf_clip = pygame.Rect(650, 471, 226, 237)
        doorway = pygame.Surface(leaf_clip.size, pygame.SRCALPHA)
        for side in (0, 1):
            left = (113 if side else 0) + round((113 if side else -113) * slide)
            pane = pygame.Rect(left, 1, 111, 234)
            pygame.draw.rect(doorway, (54, 84, 89, 222), pane)
            pygame.draw.rect(doorway, (132, 153, 149, 255), pane, 3)
            pygame.draw.line(doorway, (90, 126, 130, 255),
                             (pane.left + 11, 10), (pane.left + 11, 221), 2)
            pygame.draw.rect(doorway, (166, 175, 154, 255),
                             (pane.left + (9 if side else 92), 107, 5, 27))
        # Passa apenas depois das folhas estarem totalmente abertas.
        step = smooth((t - 12.85) / 2.03)
        if t >= 12.85:
            self._hero(screen, mix(756, 750, step), mix(707, 508, step),
                       'cima', t < 14.88, mix(.85, .59, step))
        screen.blit(doorway, leaf_clip.topleft)
        # Moldura fixa no topo e laterais preserva leitura da abertura.
        pygame.draw.rect(screen, (109, 133, 133), portal, 6)
        pygame.draw.rect(screen, (77, 107, 113), leaf_clip, 3)
        strip = pygame.Surface((WIDTH, 95), pygame.SRCALPHA)
        strip.fill((8, 12, 15, 145))
        screen.blit(strip, (0, 0))
        screen.blit(self.caption.render('RECEPCAO  /  THE LAST SHIFT', True,
                                        (222, 231, 228)), (36, 35))
        if t < self.INSIDE_START + .60:
            self._alpha_cover(screen, 1 - smooth((t - self.INSIDE_START) / .60))
        elif t > self.DURATION - .56:
            self._alpha_cover(screen, smooth((t - (self.DURATION - .56)) / .56))

    def draw(self, screen):
        t = self.elapsed
        if t < self.INSIDE_START:
            self._exterior(screen, t)
        else:
            self._inside(screen, t)
        hint = self.tiny.render('[ESPACO / ESC] PULAR ABERTURA', True,
                                (216, 219, 218))
        bg = pygame.Surface((hint.get_width() + 26, 30), pygame.SRCALPHA)
        bg.fill((9, 12, 15, 150))
        screen.blit(bg, (WIDTH - bg.get_width() - 16, HEIGHT - 44))
        screen.blit(hint, (WIDTH - hint.get_width() - 30, HEIGHT - 37))
