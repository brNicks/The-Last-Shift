import pygame


class MissionUI:

    def __init__(self):
        self.active = False
        self.title = ""
        self.message = ""
        self.timer = 0
        self.duration = 5
        self.x = 1280
        self.target_x = 920
        self.font_title = pygame.font.SysFont(None, 30)
        self.font_text = pygame.font.SysFont(None, 24)

    def show(self, title, message):
        self.active = True
        self.title = title
        self.message = message
        self.timer = 0
        self.x = 1280

    def update(self, dt):
        if not self.active:
            return
        self.timer += dt
        if self.x > self.target_x:
            self.x -= 600 * dt
        if self.timer >= self.duration:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        # Aviso limpo, sem caixa preta, para manter o cenario visivel.
        title = self.font_title.render(self.title, True, (255, 230, 100))
        text = self.font_text.render(self.message, True, (255, 255, 255))

        shadow_title = self.font_title.render(self.title, True, (20, 20, 20))
        shadow_text = self.font_text.render(self.message, True, (20, 20, 20))

        screen.blit(shadow_title, (self.x + 17, 87))
        screen.blit(shadow_text, (self.x + 17, 121))
        screen.blit(title, (self.x + 15, 85))
        screen.blit(text, (self.x + 15, 119))
