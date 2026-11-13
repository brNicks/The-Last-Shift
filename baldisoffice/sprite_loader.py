"""Carregador de sprites com atlas compacto e fallback para PNGs individuais."""
from pathlib import Path
from io import BytesIO
import base64
import json
import pygame

ROOT = Path(__file__).resolve().parent
SPRITES_DIR = ROOT / "sprites"
ATLAS_PATH = SPRITES_DIR / "sprite_atlas.b64"
MANIFEST_PATH = SPRITES_DIR / "sprite_manifest.json"
_CACHE = {}
_SCALE_CACHE = {}
_ATLAS = None
_MANIFEST = None


def _load_atlas():
    global _ATLAS, _MANIFEST
    if _ATLAS is None:
        try:
            raw = base64.b64decode(ATLAS_PATH.read_text(encoding="ascii"))
            _ATLAS = pygame.image.load(BytesIO(raw), "sprite_atlas.png").convert_alpha()
            with MANIFEST_PATH.open("r", encoding="utf-8") as file:
                _MANIFEST = json.load(file)
        except (pygame.error, OSError, ValueError):
            _ATLAS = False
            _MANIFEST = {}
    return _ATLAS


def load_sprite(relative_path):
    key = relative_path.replace("\\", "/")
    if key not in _CACHE:
        atlas = _load_atlas()
        entry = (_MANIFEST or {}).get(key) if atlas else None
        if entry:
            rect = pygame.Rect(entry["x"], entry["y"], entry["w"], entry["h"])
            _CACHE[key] = atlas.subsurface(rect).copy()
        else:
            # Permite adicionar sprites individuais sem depender do atlas completo.
            image_path = SPRITES_DIR / key
            try:
                _CACHE[key] = pygame.image.load(str(image_path)).convert_alpha()
            except (pygame.error, OSError):
                _CACHE[key] = None
    return _CACHE[key]


def load_animation(folder):
    frames = []
    index = 0
    while True:
        frame = load_sprite(f"{folder}/{index}.png")
        if frame is None:
            break
        frames.append(frame)
        index += 1
    return frames


def draw_character(screen, image, rect, camera, size):
    if image is None:
        return False
    scale_key = (id(image), size)
    if scale_key not in _SCALE_CACHE:
        _SCALE_CACHE[scale_key] = pygame.transform.smoothscale(image, size)
    scaled = _SCALE_CACHE[scale_key]
    x = rect.centerx - size[0] // 2
    y = rect.bottom - size[1]
    if camera is not None:
        x -= camera.offset_x
        y -= camera.offset_y
    screen.blit(scaled, (x, y))
    return True
