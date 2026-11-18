import pygame
from settings import TILE_SIZE, GRAY
class GameMap:
    def __init__(self):
        self.layout=[
            "########################","#......................#","#......................#",
            "#....######............#","#......................#","#...........#########..#",
            "#......................#","#......................#","#......................#",
            "########################"]
        self.walls=[]; self.create_walls()
    def create_walls(self):
        for ri,row in enumerate(self.layout):
            for ci,tile in enumerate(row):
                if tile=="#": self.walls.append(pygame.Rect(ci*TILE_SIZE,ri*TILE_SIZE,TILE_SIZE,TILE_SIZE))
    def draw(self,screen,camera):
        for ri,row in enumerate(self.layout):
            for ci,tile in enumerate(row):
                rect=pygame.Rect(ci*TILE_SIZE,ri*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                pygame.draw.rect(screen,(60,60,60),camera.apply_rect(rect))
        for wall in self.walls: pygame.draw.rect(screen,GRAY,camera.apply_rect(wall))
