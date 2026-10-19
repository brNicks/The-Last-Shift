import pygame


class DialogueBox:

    def __init__(self):
        self.active = False
        self.full_text = ""
        self.current_text = ""
        self.char_index = 0
        self.typing_speed = 0.03
        self.type_timer = 0
        self.close_timer = 0
        self.duration = 2
        self.font = pygame.font.SysFont(None, 30)

    def show(self, text):
        self.active = True
        self.full_text = text
        self.current_text = ""
        self.char_index = 0
        self.type_timer = 0
        self.close_timer = 0

    def hide(self):
        self.active = False

    def update(self, dt):
        if not self.active:
            return
        if self.char_index < len(self.full_text):
            self.type_timer += dt
            if self.type_timer >= self.typing_speed:
                self.current_text += self.full_text[self.char_index]
                self.char_index += 1
                self.type_timer = 0
        else:
            self.close_timer += dt
            if self.close_timer >= self.duration:
                self.hide()

    def draw(self, screen):
        if not self.active:
            return

        # Mensagem simples: sem painel preto, para nao esconder o cenario.
        shadow = self.font.render(self.current_text, True, (15, 15, 15))
        text = self.font.render(self.current_text, True, (255, 255, 255))

        x = 60
        y = 665
        screen.blit(shadow, (x + 2, y + 2))
        screen.blit(text, (x, y))
