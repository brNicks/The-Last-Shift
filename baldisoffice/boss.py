import pygame
from sprite_loader import load_animation, load_sprite, draw_character


class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 42, 42)
        self.speed = 1.35
        self.active = False
        self.chasing = False
        self.facing = "down"
        self.animation_timer = 0.0
        self.animation_frame = 0
        self.stage = 0
        self.animations = {
            "down": load_animation("boss/move_down"),
            "up": load_animation("boss/move_up"),
            "left": load_animation("boss/move_left"),
            "right": load_animation("boss/move_right"),
            "run": load_animation("boss/move_run"),
            "idle": load_animation("boss/move_idle"),
        }
        self.stage_sprites = [
            load_sprite("boss/stages/calmo.png"),
            load_sprite("boss/stages/irritado.png"),
            load_sprite("boss/stages/estranho.png"),
            load_sprite("boss/stages/voz_alterada.png"),
            load_sprite("boss/stages/insano.png"),
        ]

    def activate(self):
        self.active = True

    def update(self, target_rect, dt):
        if not self.active:
            return

        direction = pygame.Vector2(
            target_rect.centerx - self.rect.centerx,
            target_rect.centery - self.rect.centery
        )

        if direction.length_squared() > 0:
            if abs(direction.x) > abs(direction.y):
                self.facing = "right" if direction.x > 0 else "left"
            else:
                self.facing = "down" if direction.y > 0 else "up"
            direction = direction.normalize()
            self.rect.x += int(direction.x * self.speed * dt * 60)
            self.rect.y += int(direction.y * self.speed * dt * 60)

        self.animation_timer += dt
        if self.animation_timer >= (0.11 if self.chasing else 0.17):
            self.animation_timer = 0.0
            self.animation_frame += 1

    def draw(self, screen, camera=None, stage=None):
        if not self.active:
            return

        # O estágio 0 também é uma transformação válida: Calmo.
        # Só usa animação direcional quando nenhum estágio foi informado.
        if stage is not None:
            stage_index = max(0, min(4, int(stage)))
            image = self.stage_sprites[stage_index]
        else:
            key = "run" if self.chasing else self.facing
            frames = self.animations.get(key, [])
            if not frames:
                frames = self.animations.get("idle", [])
            image = frames[self.animation_frame % len(frames)] if frames else None

        if not draw_character(screen, image, self.rect, camera, (72, 112)):
            target = camera.apply_rect(self.rect) if camera else self.rect
            pygame.draw.rect(screen, (150, 20, 20), target)
