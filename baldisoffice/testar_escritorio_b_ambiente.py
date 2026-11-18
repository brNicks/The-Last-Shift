"""Atalho de teste isolado: entra no B sem alterar Game ou as missoes originais."""
import pygame
from game import Game

if __name__ == '__main__':
    pygame.init()
    try:
        game = Game()
        game.game_state = 'GAME'
        game.enter_office('B')
        game.player.rect.topleft = (145, 510)
        game.objective = 'Encontre os 3 documentos'
        game.mission_ui.show('TESTE VISUAL B', 'Explore, colete e avalie normalmente')
        game.run()
    finally:
        pygame.quit()
