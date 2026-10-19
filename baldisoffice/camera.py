import pygame
from settings import *

class Camera:

    def __init__(self):

        self.offset_x = 0
        self.offset_y = 0

    def update(self, target):

        self.offset_x = target.centerx - WIDTH // 2
        self.offset_y = target.centery - HEIGHT // 2

    def apply_rect(self, rect):

        return rect.move(
            -self.offset_x,
            -self.offset_y
        )