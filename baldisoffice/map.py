import pygame
from settings import *

class GameMap:

    def __init__(self):

        self.layout = [

            "########################",
            "#......................#",
            "#......................#",
            "#....######............#",
            "#......................#",
            "#...........#########..#",
            "#......................#",
            "#......................#",
            "#......................#",
            "########################"

        ]

        self.walls = []

        self.create_walls()

    def create_walls(self):

        for row_index, row in enumerate(self.layout):

            for col_index, tile in enumerate(row):

                if tile == "#":

                    wall = pygame.Rect(

                        col_index * TILE_SIZE,
                        row_index * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE

                    )

                    self.walls.append(wall)

    def draw(self, screen, camera):

        for row_index, row in enumerate(self.layout):

            for col_index, tile in enumerate(row):

                rect = pygame.Rect(

                    col_index * TILE_SIZE,
                    row_index * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE

                )

                pygame.draw.rect(

                    screen,
                    (60,60,60),
                    camera.apply_rect(rect)

                )

        for wall in self.walls:

            pygame.draw.rect(

                screen,
                GRAY,
                camera.apply_rect(wall)

            )