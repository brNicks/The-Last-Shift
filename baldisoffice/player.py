import pygame

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

    def draw(self, screen, camera):

        pygame.draw.rect(

            screen,
            BLUE,
            camera.apply_rect(self.rect)

        )