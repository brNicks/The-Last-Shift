"""Inicia dentro do Escritorio A para revisar apenas o polimento visual."""
import pygame
from game import Game

if __name__ == "__main__":
    pygame.init()
    try:
        jogo = Game()
        jogo.enter_office("A")
        jogo.game_state = "GAME"  # Atalho de teste: pula somente o menu.
        jogo.run()
    finally:
        pygame.quit()
