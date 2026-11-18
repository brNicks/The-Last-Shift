"""V62 Parte 14: teste RAPIDO do Escritorio B no jogo real.
Este arquivo NAO altera a V61 nem o game.py. Entrada de depuracao isolada.
"""
import sys
import pygame
from game import Game

def testar(modo):
    pygame.init()
    try:
        game = Game()
        game.game_state = 'GAME'
        game.enter_office('B')
        # Pula apenas a coleta de documentos no modo de teste, sem alterar
        # codigo de objetivo, IA, sprites ou colisoes do jogo principal.
        for doc in game.b_documents:
            doc.collected = True
        game.documents_collected = 3

        if modo == 'avaliacao':
            # A avaliacao e a mesma do jogo principal, com 10 perguntas.
            game.player.rect.topleft = (800, 385)
            game.start_evaluation()
            game.mission_ui.show('TESTE ESCRITORIO B', '1 a 4: responda 10 questoes')
        elif modo == 'revelacao':
            # Comeca na pausa de suspense (4,5 s) que sucede a avaliacao.
            # O update() original ativa o chefe e a perseguicao automaticamente.
            game.player.rect.topleft = (155, 520)
            game.b_tension = game.b_tension_max
            game.b_tension_stage = 5
            game.math.active = False
            game.evaluation_started = False
            game.evaluation_finished = True
            game.b_boss_reveal_pending = True
            game.b_boss_reveal_timer = game.b_boss_reveal_duration
            game.boss_active = False
            game.boss.active = False
            game.boss_state = 'idle'
            game.b_insane_active = False
            game.b_exit_unlocked = False
            game.objective = '...'
            game.mission_ui.show('TESTE REVELACAO B', 'Observe a entrada do chefe Insano')
        else:
            raise ValueError('Modo invalido: ' + str(modo))
        game.run()
    finally:
        pygame.quit()

if __name__ == '__main__':
    try:
        testar(sys.argv[1] if len(sys.argv) > 1 else 'avaliacao')
    except Exception:
        import traceback
        traceback.print_exc()
        raise
