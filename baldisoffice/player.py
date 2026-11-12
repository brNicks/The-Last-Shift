import pygame
from sprite_loader import load_animation, draw_character

from settings import *

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(

            x,
            y,
            PLAYER_SIZE,
            PLAYER_SIZE

        )

        self.stamina = MAX_STAMINA
        self.facing = "down"
        self.moving = False
        self.running = False
        self.interacting = False
        self.animation_timer = 0.0
        self.animation_frame = 0
        self.animations = {
            "down": load_animation("player/down"),
            "up": load_animation("player/up"),
            "left": load_animation("player/left"),
            "right": load_animation("player/right"),
            "run": load_animation("player/run"),
            "idle": load_animation("player/idle"),
            "interact": load_animation("player/interact"),
        }

    def update(self, walls, dt):

        keys = pygame.key.get_pressed()

        speed = WALK_SPEED

        moving = False

        if keys[pygame.K_LSHIFT] and self.stamina > 0:
            speed = RUN_SPEED
            self.stamina -= RUN_COST * dt

        dx = 0
        dy = 0

        if keys[pygame.K_w]:

            dy = -speed
            moving = True

        if keys[pygame.K_s]:

            dy = speed
            moving = True

        if keys[pygame.K_a]:

            dx = -speed
            moving = True

        if keys[pygame.K_d]:

            dx = speed
            moving = True

        if speed == WALK_SPEED:

            if moving:

                self.stamina += WALK_RECOVERY * dt

            else:

                self.stamina += IDLE_RECOVERY * dt

        self.stamina = max(
            0,
            min(MAX_STAMINA, self.stamina)
        )

        self.rect.x += dx

        for wall in walls:

            if self.rect.colliderect(wall):

                if dx > 0:
                    self.rect.right = wall.left

                if dx < 0:
                    self.rect.left = wall.right

        self.rect.y += dy

        for wall in walls:

            if self.rect.colliderect(wall):

                if dy > 0:
                    self.rect.bottom = wall.top

                if dy < 0:
                    self.rect.top = wall.bottom

        self.moving = moving
        if dx < 0:
            self.facing = "left"
        elif dx > 0:
            self.facing = "right"
        elif dy < 0:
            self.facing = "up"
        elif dy > 0:
            self.facing = "down"

        self.running = bool(moving and speed == RUN_SPEED)
        self.interacting = bool(keys[pygame.K_e] and not moving)

        self.animation_timer += dt
        frame_delay = 0.10 if self.running else 0.16
        if self.animation_timer >= frame_delay:
            self.animation_timer = 0.0
            self.animation_frame += 1

    def draw(self, screen, camera):
        if self.interacting:
            frames = self.animations["interact"]
        elif self.running:
            frames = self.animations["run"]
        elif self.moving:
            frames = self.animations.get(self.facing, [])
        else:
            frames = self.animations["idle"]

        if frames:
            image = frames[self.animation_frame % len(frames)]
            if draw_character(screen, image, self.rect, camera, (58, 94)):
                return

        pygame.draw.rect(screen, BLUE, camera.apply_rect(self.rect))