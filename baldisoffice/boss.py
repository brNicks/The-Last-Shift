import pygame


class Boss:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 42, 42)

        # Velocidade inicial do chefe.
        self.speed = 1.35

        # O chefe começa escondido/inativo.
        self.active = False

        # Quando começa a perseguir de verdade.
        self.chasing = False

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
            direction = direction.normalize()

            self.rect.x += int(direction.x * self.speed * dt * 60)
            self.rect.y += int(direction.y * self.speed * dt * 60)

    def draw(self, screen):
        if not self.active:
            return

        # Corpo do chefe.
        pygame.draw.rect(
            screen,
            (150, 20, 20),
            self.rect
        )

        # Olhos.
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.rect.x + 8, self.rect.y + 9, 8, 8)
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (self.rect.x + 26, self.rect.y + 9, 8, 8)
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (self.rect.x + 10, self.rect.y + 27, 22, 5)
        )
