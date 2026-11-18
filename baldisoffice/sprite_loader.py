# Compatibilidade com os módulos legados da V61.
# A renderização principal das sprites V62 é feita por CharacterSpriteRenderer em game.py.
from pathlib import Path
import pygame
ROOT=Path(__file__).resolve().parent
SPRITES_DIR=ROOT/'sprites'
_CACHE={}
def load_sprite(relative_path):
    key=relative_path.replace('\\\\','/')
    if key not in _CACHE:
        path=SPRITES_DIR/key
        try: _CACHE[key]=pygame.image.load(str(path)).convert_alpha()
        except (pygame.error,OSError): _CACHE[key]=None
    return _CACHE[key]
def load_animation(folder):
    frames=[]; index=0
    while True:
        frame=load_sprite(f'{folder}/{index}.png')
        if frame is None: break
        frames.append(frame); index+=1
    return frames
def draw_character(screen,image,rect,camera,size):
    if image is None: return False
    scaled=pygame.transform.smoothscale(image,size)
    target=rect.copy()
    if camera is not None: target=camera.apply_rect(rect)
    screen.blit(scaled,(target.centerx-size[0]//2,target.bottom-size[1]))
    return True
