import pygame
import random
import math

from settings import *

from player import Player
from map import GameMap
from camera import Camera

from npc import NPC
from dialogue import DialogueBox
from item import Item

from mission_ui import MissionUI
from door import Door

from math_challenge import MathChallenge
from boss import Boss


class Game:

    def __init__(self):

        # =========================
        # TELA
        # =========================

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "The Last Shift"
        )

        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont(
            None,
            30
        )

        self.big_font = pygame.font.SysFont(
            None,
            42
        )

        # =========================
        # MENU INICIAL
        # =========================
        self.game_state = "MENU"
        self.menu_selected = 0
        self.menu_glitch_timer = 0
        self.menu_flicker_timer = 0
        self.menu_time = 0.0
        self.menu_option_rects = []
        self.menu_mouse_active = False

        # =========================
        # MAPA
        # =========================

        self.map = GameMap()

        # =========================
        # JOGADOR
        # =========================

        self.player = Player(
            150,
            150
        )

        self.camera = Camera()

        # =========================
        # CLARA
        # =========================

        self.clara = NPC(
            350,
            200,
            "Clara",
            "Voce finalmente chegou. Pegue seu cracha."
        )

        self.talked_to_clara = False

        # =========================
        # SISTEMAS
        # =========================

        self.dialogue = DialogueBox()

        self.mission_ui = MissionUI()

        # =========================
        # OBJETIVO
        # =========================

        self.objective = "Falar com Clara"

        self.mission_ui.show(
            "NOVA MISSAO",
            "Falar com Clara"
        )

        # =========================
        # CRACHÁ
        # =========================

        self.badge = Item(
            600,
            250,
            "Cracha"
        )

        self.has_badge = False

        # =========================
        # PORTA DO ESCRITÓRIO A
        # =========================

        # Portas lado a lado na recepcao: A primeiro, B depois.
        self.office_door = Door(900, 320)
        self.office_b_door = Door(1024, 320)
        self.office_b_unlocked = False

        # =========================
        # DOCUMENTOS
        # =========================

        self.doc1 = Item(
            300,
            250,
            "Documento 1"
        )

        self.doc2 = Item(
            600,
            250,
            "Documento 2"
        )

        self.doc3 = Item(
            900,
            250,
            "Documento 3"
        )

        self.documents_collected = 0

        # =========================
        # AVALIAÇÃO
        # =========================

        self.math = MathChallenge()

        self.math_station = pygame.Rect(
            570,
            400,
            140,
            80
        )

        # =========================
        # OBSTÁCULOS - ESCRITÓRIO A
        # =========================
        self.office_a_obstacles = [
            # Mesas superiores ainda mais baixas para deixar uma faixa livre
            # entre as mesas e as luminarias do teto.
            pygame.Rect(180, 260, 120, 150),
            pygame.Rect(390, 250, 190, 75),
            pygame.Rect(700, 270, 190, 75),
            # Mesa lateral permanece na mesma regiao, pois nao encosta nas luzes.
            pygame.Rect(950, 330, 100, 150),
            # Mesas inferiores acompanhando o novo equilibrio visual.
            pygame.Rect(350, 475, 170, 70),
            pygame.Rect(720, 505, 180, 70),
        ]
        self.office_b_obstacles = [
            # Mesas superiores: faixa livre entre elas e as luminárias.
            pygame.Rect(150, 225, 180, 70),
            pygame.Rect(420, 215, 120, 180),
            pygame.Rect(660, 235, 210, 70),
            # Mesa lateral direita.
            pygame.Rect(930, 350, 150, 80),
            # Mesas inferiores.
            pygame.Rect(300, 465, 180, 70),
            pygame.Rect(620, 445, 120, 180),
        ]
        self.office_obstacles = self.office_a_obstacles
        self.a_documents = [self.doc1, self.doc2, self.doc3]
        self.b_doc1 = Item(260, 300, "Documento B1")
        self.b_doc2 = Item(580, 280, "Documento B2")
        self.b_doc3 = Item(1110, 500, "Documento B3")
        self.b_documents = [self.b_doc1, self.b_doc2, self.b_doc3]
        self.b_math_station = pygame.Rect(900, 245, 140, 80)
        self.office_a_exit = pygame.Rect(1080, 560, 120, 80)
        self.office_b_exit = pygame.Rect(1080, 560, 120, 80)
        self.current_office = "A"
        self.recovery_mode = False
        self.office_a_passed = False
        self.office_b_passed = False

        # True enquanto a interface da avaliação está aberta.
        self.evaluation_started = False

        # Indica que a avaliação já foi iniciada pelo menos uma vez.
        # Isso permite sair com ESC e depois continuar sem reiniciar as questões.
        self.evaluation_has_started = False

        self.evaluation_finished = False
        self.evaluation_intro_timer = 0.0
        self.evaluation_intro_duration = 1.15
        self.b_corruption_level = 0
        self.b_question_number = 0
        self.b_question_answered = False
        self.b_evaluation_complete = False
        self.b_corruption_anim_timer = 0.0

        # =========================
        # SISTEMA DE TENSÃO / CHEFE
        # =========================

        self.anger = 0
        self.max_anger = 5

        # O chefe aparece depois de erros suficientes.
        self.boss = Boss(
            1050,
            180
        )

        self.boss_active = False
        self.game_over = False

        # Estados da IA:
        # idle, patrol, heard, search, chase e insane.
        self.boss_state = "idle"

        # Patrulha livre.
        self.boss_roam_target = None
        self.boss_roam_wait = 0.0

        self.boss_search_timer = 0
        self.boss_last_seen = None

        # =========================
        # PERCEPÇÃO DO CHEFE
        # =========================
        self.boss_vision_radius = 300

        # Audição: correr faz mais barulho.
        self.boss_hearing_walk_radius = 125
        self.boss_hearing_run_radius = 260

        self.boss_lost_sight_time = 2.0
        self.boss_lost_sight_timer = 0.0
        self.boss_search_duration = 4.0

        self.boss_alert_text = ""
        self.boss_alert_timer = 0.0

        # =========================
        # NAVEGAÇÃO DO CHEFE
        # =========================
        # O chefe não atravessa móveis e também não fica
        # tentando andar eternamente contra o mesmo obstáculo.
        self.boss_path = []
        self.boss_path_target = None
        self.boss_path_timer = 0.0
        self.boss_path_recalculate = 0.25

        # =========================
        # CHECKPOINT - ESCRITORIO A
        # =========================
        self.checkpoint_active = False
        self.checkpoint_timer = 0
        self.checkpoint_duration = 2.0

        # =========================
        # SAÍDA
        # =========================

        self.exit_rect = pygame.Rect(
            1080,
            560,
            120,
            80
        )

        # =========================
        # ESTADO
        # =========================

        self.current_room = "office"

        self.interaction_text = ""
        self.interaction_rect = None

        self.running = True

        # A Fase 1 só termina depois que o jogador escapa do B,
        # retorna à recepção e fala com Clara.
        self.phase1_return_pending = False

        # Suspense entre a última questão e a primeira aparição do chefe.
        self.b_boss_reveal_pending = False
        self.b_boss_reveal_timer = 0.0
        self.b_boss_reveal_duration = 4.5

        # Pequena transicao visual depois de escapar do chefe.
        self.escape_transition_timer = 0.0
        self.escape_transition_duration = 1.15

        # Encerramento narrativo da Fase 1 depois de falar com Clara.
        self.phase1_ending_timer = 0.0
        self.phase1_ending_duration = 14.0

        # =========================
        # OBJETOS EXAMINAVEIS / EVENTOS RAROS
        # =========================
        self.exam_objects = {
            "relogio_a": {"rect": pygame.Rect(615, 180, 58, 36), "text": "O relogio esta funcionando normalmente."},
            # O computador acompanha a mesa superior direita rebaixada.
            "computador_a": {"rect": pygame.Rect(750, 230, 68, 40), "text": "O computador esta desligado."},
            "relogio_b": {"rect": pygame.Rect(1030, 115, 58, 36), "text": "O relogio marca o horario normal."},
            "monitor_b": {"rect": pygame.Rect(742, 125, 68, 40), "text": "O monitor esta ligado. Nao ha ninguem usando esta maquina."},
        }
        self.b_ambient_event_timer = 0.0
        self.b_ambient_event_cooldown = 10.0
        self.b_ambient_event_active = False
        self.b_ambient_event_duration = 1.1
        self.b_ambient_event_shift = 0
        self.b_ambient_event_type = 0

        self.victory = False

    # =====================================================
    # LOOP PRINCIPAL
    # =====================================================


    # =====================================================
    # MENU INICIAL
    # =====================================================

    def draw_menu(self):
        # =====================================================
        # MENU INICIAL — GLITCH / CORRUPÇÃO VISUAL
        # =====================================================
        now = pygame.time.get_ticks()

        # Fundo escuro de escritório.
        self.screen.fill((8, 9, 11))

        # -----------------------------------------------------
        # GRADE CORPORATIVA
        # -----------------------------------------------------
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(self.screen, (21, 22, 25), (0, y), (WIDTH, y), 1)
        for x in range(0, WIDTH, 80):
            pygame.draw.line(self.screen, (18, 19, 22), (x, 0), (x, HEIGHT), 1)

        horizon = HEIGHT // 2 + 30
        for x in range(0, WIDTH + 1, 120):
            pygame.draw.line(
                self.screen, (19, 20, 23),
                (WIDTH // 2, horizon), (x, HEIGHT), 1
            )

        # -----------------------------------------------------
        # ESCRITÓRIO AO FUNDO
        # -----------------------------------------------------
        furniture = (16, 17, 20)
        pygame.draw.rect(self.screen, furniture, (70, 410, 190, 55))
        pygame.draw.rect(self.screen, furniture, (780, 390, 210, 65))
        pygame.draw.rect(self.screen, furniture, (330, 470, 120, 35))
        pygame.draw.rect(self.screen, furniture, (520, 455, 160, 45))

        for x in (170, 550, 930):
            pygame.draw.rect(self.screen, (14, 15, 18), (x, 80, 5, 330))

        # -----------------------------------------------------
        # GLITCH CONTROLADO
        # -----------------------------------------------------
        # O efeito aparece em pequenos intervalos, mas é mais perceptível
        # que na versão anterior. Ele não fica constante para não cansar.
        glitch_cycle = now % 5200
        glitch_active = glitch_cycle < 220 or (2700 <= glitch_cycle < 2820)
        strong_glitch = glitch_cycle < 95

        # Semente baseada no tempo para o glitch ficar estável durante
        # alguns frames em vez de trocar aleatoriamente a cada frame.
        rng = random.Random(now // 45)

        # Linhas de varredura muito discretas.
        for y in range(0, HEIGHT, 4):
            pygame.draw.line(self.screen, (13, 14, 16), (0, y), (WIDTH, y), 1)

        # Pequenas falhas horizontais atravessando a imagem.
        if glitch_active:
            amount = 9 if strong_glitch else 4
            for _ in range(amount):
                y = rng.randint(80, HEIGHT - 80)
                h = rng.randint(1, 5 if strong_glitch else 3)
                shift = rng.randint(-28, 28) if strong_glitch else rng.randint(-14, 14)

                strip = self.screen.subsurface(
                    pygame.Rect(0, y, WIDTH, min(h, HEIGHT - y))
                ).copy()
                self.screen.blit(strip, (shift, y))

                # Pequeno risco de interferência.
                if rng.random() < 0.7:
                    pygame.draw.rect(
                        self.screen,
                        (55, 56, 60),
                        (rng.randint(0, WIDTH - 60), y, rng.randint(20, 100), 1)
                    )

        # -----------------------------------------------------
        # TÍTULO
        # -----------------------------------------------------
        title_font = pygame.font.SysFont(None, 78)
        subtitle_font = pygame.font.SysFont(None, 22)
        option_font = pygame.font.SysFont(None, 36)
        small_font = pygame.font.SysFont(None, 19)

        title = title_font.render("THE LAST SHIFT", True, (235, 235, 235))
        title_rect = title.get_rect(center=(WIDTH // 2, 155))

        # Pequena tremida do título durante a corrupção.
        title_x = title_rect.x
        title_y = title_rect.y
        if glitch_active:
            title_x += rng.randint(-4, 4) if strong_glitch else rng.randint(-2, 2)
            title_y += rng.randint(-2, 2)

        # Duplicações deslocadas simulando canais quebrados.
        if glitch_active:
            ghost = title_font.render("THE LAST SHIFT", True, (70, 80, 82))
            ghost.set_alpha(110)
            self.screen.blit(ghost, (title_x + rng.randint(-8, 8), title_y + 3))

            if strong_glitch:
                ghost2 = title_font.render("THE LAST SHIFT", True, (120, 120, 120))
                ghost2.set_alpha(95)
                self.screen.blit(ghost2, (title_x - 5, title_y - 2))

        # Às vezes o título sofre um pequeno "salto" lateral.
        self.screen.blit(title, (title_x, title_y))

        # Barras de glitch sobre partes do título.
        if glitch_active:
            for _ in range(2 if not strong_glitch else 5):
                gy = rng.randint(title_y + 12, title_y + 62)
                gx = rng.randint(title_x - 10, title_x + title.get_width() - 20)
                gw = rng.randint(20, 110)
                pygame.draw.rect(self.screen, (150, 150, 150), (gx, gy, gw, 2))

        pygame.draw.line(
            self.screen, (85, 85, 88),
            (WIDTH // 2 - 190, 210),
            (WIDTH // 2 + 190, 210), 1
        )

        subtitle = subtitle_font.render(
            "EMPRESA  /  PRIMEIRO TURNO  /  ARQUIVO INTERNO",
            True, (115, 115, 118)
        )
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 235)))

        # -----------------------------------------------------
        # BOTÕES
        # -----------------------------------------------------
        options = ["JOGAR", "SAIR"]
        self.menu_option_rects = []
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(options):
            rect = pygame.Rect(0, 0, 260, 50)
            rect.center = (WIDTH // 2, 345 + i * 65)
            self.menu_option_rects.append(rect)

            hovered = rect.collidepoint(mouse_pos)
            if hovered:
                self.menu_selected = i
                self.menu_mouse_active = True

            selected = (i == self.menu_selected)
            pulse = int(4 * (0.5 + 0.5 * math.sin(now / 180)))

            color = (245, 245, 245) if selected else (105, 105, 108)
            label = option_font.render(option, True, color)
            label_rect = label.get_rect(center=rect.center)

            if selected:
                outline = rect.inflate(18 + pulse, 8)
                pygame.draw.rect(self.screen, (35, 36, 39), outline, 1)
                pygame.draw.line(
                    self.screen, (175, 175, 178),
                    (label_rect.left - 30, label_rect.centery),
                    (label_rect.left - 12, label_rect.centery), 2
                )
                pygame.draw.line(
                    self.screen, (175, 175, 178),
                    (label_rect.right + 12, label_rect.centery),
                    (label_rect.right + 30, label_rect.centery), 2
                )

            self.screen.blit(label, label_rect)

            # Glitch ocasional somente na opção selecionada.
            if glitch_active and selected and strong_glitch:
                broken = option_font.render(option, True, (115, 115, 115))
                broken.set_alpha(130)
                self.screen.blit(broken, (label_rect.x + rng.randint(-5, 5), label_rect.y + 2))

        # -----------------------------------------------------
        # TEXTO DE AMBIENTAÇÃO
        # -----------------------------------------------------
        hint = small_font.render(
            "Seu primeiro turno deveria ser apenas o começo.",
            True, (72, 72, 75)
        )
        self.screen.blit(hint, hint.get_rect(center=(WIDTH // 2, 510)))

        controls = subtitle_font.render(
            "[W/S ou ↑/↓] SELECIONAR     [ENTER/ESPAÇO] CONFIRMAR     [ESC] SAIR",
            True, (78, 78, 80)
        )
        self.screen.blit(controls, controls.get_rect(center=(WIDTH // 2, HEIGHT - 42)))

        version = small_font.render("THE LAST SHIFT  •  FASE 1", True, (55, 55, 58))
        self.screen.blit(version, (22, HEIGHT - 28))

        # -----------------------------------------------------
        # INTERFERÊNCIA FINAL
        # -----------------------------------------------------
        if strong_glitch:
            # Uma faixa rápida corta a tela, dando a sensação de imagem
            # deslocada sem esconder completamente o menu.
            for _ in range(3):
                y = rng.randint(0, HEIGHT - 3)
                h = rng.randint(1, 3)
                pygame.draw.rect(self.screen, (90, 90, 94), (0, y, WIDTH, h))

    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.menu_selected = (self.menu_selected - 1) % 2
                self.menu_mouse_active = False

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.menu_selected = (self.menu_selected + 1) % 2
                self.menu_mouse_active = False

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.menu_selected == 0:
                    # Começa exatamente a Fase 1 existente.
                    self.game_state = "GAME"
                    self.mission_ui.show(
                        "NOVA MISSAO",
                        "Falar com Clara"
                    )
                else:
                    pygame.quit()
                    raise SystemExit

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit

        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.menu_option_rects):
                if rect.collidepoint(event.pos):
                    self.menu_selected = i
                    self.menu_mouse_active = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.menu_option_rects):
                if rect.collidepoint(event.pos):
                    self.menu_selected = i
                    if i == 0:
                        self.game_state = "GAME"
                        self.mission_ui.show(
                            "NOVA MISSAO",
                            "Falar com Clara"
                        )
                    else:
                        pygame.quit()
                        raise SystemExit

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000

            self.events()

            if self.game_state == "MENU":
                self.draw_menu()
                pygame.display.flip()
            else:
                self.update(dt)
                self.draw()

    def events(self):

        for event in pygame.event.get():
            if self.game_state == "MENU":
                self.handle_menu_event(event)
                continue


            # -------------------------
            # FECHAR JOGO
            # -------------------------

            if event.type == pygame.QUIT:

                self.running = False

            # -------------------------
            # TECLAS
            # -------------------------

            elif event.type == pygame.KEYDOWN:

                # ESC
                if event.key == pygame.K_ESCAPE:

                    # ESC fecha somente a interface da avaliação.
                    # O progresso da prova e o chefe continuam ativos.
                    if self.math.active:
                        self.math.active = False
                        self.evaluation_started = False

                    self.dialogue.hide()

                # =====================
                # AVALIAÇÃO
                # =====================

                elif self.math.active:

                    if event.key == pygame.K_1:

                        self.answer_question(0)

                    elif event.key == pygame.K_2:

                        self.answer_question(1)

                    elif event.key == pygame.K_3:

                        self.answer_question(2)

                    elif event.key == pygame.K_4:

                        self.answer_question(3)

                # =====================
                # INTERAÇÃO
                # =====================

                elif event.key == pygame.K_e:

                    self.handle_interaction()

    # =====================================================
    # INTERAÇÕES
    # =====================================================

    def handle_interaction(self):

        if self.game_over or self.checkpoint_active:
            return

        # =========================
        # SALA PRINCIPAL
        # =========================

        if self.current_room == "office":

            # -------------------------
            # CLARA
            # -------------------------

            if self.player.rect.colliderect(
                self.clara.rect.inflate(80, 80)
            ):

                # Depois de escapar do B, falar com Clara encerra a Fase 1.
                if self.phase1_return_pending:
                    self.phase1_return_pending = False
                    self.office_b_passed = True
                    self.victory = True
                    self.phase1_ending_timer = 0.0
                    self.objective = "FASE 1 CONCLUIDA"

                    self.dialogue.show(
                        "Voce sobreviveu ao seu primeiro turno..."
                    )

                    self.mission_ui.show(
                        "FASE CONCLUIDA",
                        "Voce terminou a Fase 1."
                    )
                    return

                self.dialogue.show(
                    self.clara.dialogue
                )

                if not self.talked_to_clara:

                    self.talked_to_clara = True

                    self.objective = "Pegar o cracha"

                    self.mission_ui.show(
                        "NOVA MISSAO",
                        "Pegar o cracha"
                    )

                return

            # -------------------------
            # CRACHÁ
            # -------------------------

            if (
                self.talked_to_clara
                and not self.badge.collected
                and self.player.rect.colliderect(
                    self.badge.rect.inflate(80, 80)
                )
            ):

                self.badge.collected = True

                self.has_badge = True

                self.objective = (
                    "Entrar no Escritorio A"
                )

                self.dialogue.show(
                    "Cracha obtido!"
                )

                self.mission_ui.show(
                    "NOVA MISSAO",
                    "Entrar no Escritorio A"
                )

                return

            # -------------------------
            # PORTA
            # -------------------------

            if self.has_badge and self.player.rect.colliderect(self.office_door.rect.inflate(80, 80)):
                self.enter_office("A")
                return

            if self.office_b_unlocked and self.player.rect.colliderect(self.office_b_door.rect.inflate(80, 80)):
                self.enter_office("B")
                return

        # =========================
        # ESCRITÓRIOS A / B
        # =========================
        elif self.current_room in ("office_a", "office_b"):
            documents = self.get_current_documents()
            station = self.get_current_station()
            exit_rect = self.get_current_exit()
            if not self.evaluation_started and self.documents_collected < 3:
                for doc in documents:
                    if not doc.collected and self.player.rect.colliderect(doc.rect.inflate(60, 60)):
                        doc.collected=True; self.documents_collected+=1

                        if self.current_office == "B":
                            clue_messages = {
                                "Documento B1": "Documento B1 coletado. O relatorio parece normal... quase.",
                                "Documento B2": "Documento B2 coletado. Ha informacoes aqui que voce nao deveria estar lendo.",
                                "Documento B3": "Documento B3 coletado. Por que seu nome aparece neste documento?",
                            }
                            self.dialogue.show(clue_messages.get(doc.name, f"{doc.name} coletado!"))
                        else:
                            # Polimento narrativo da Fase 1: os documentos do
                            # Escritório A parecem profissionais, mas deixam
                            # pequenas dúvidas sem antecipar o terror do B.
                            a_clue_messages = {
                                "Documento 1": "Documento 1 coletado. Relatorio de rotina: tudo parece em ordem.",
                                "Documento 2": "Documento 2 coletado. Ha um horario anotado que nao combina com o expediente.",
                                "Documento 3": "Documento 3 coletado. O campo de assinatura esta preenchido, mas voce nao reconhece o nome.",
                            }
                            self.dialogue.show(
                                a_clue_messages.get(doc.name, f"{doc.name} coletado!")
                            )

                        if self.documents_collected==3:
                            self.objective="Ir ate a estacao de avaliacao"
                            self.mission_ui.show("DOCUMENTOS","Va ate a estacao de avaliacao")
                            # V57: pequena conclusao narrativa da busca no Escritorio A.
                            if self.current_office == "A":
                                self.dialogue.show(
                                    "Os tres documentos estao reunidos. "
                                    "A assinatura desconhecida continua na sua cabeca."
                                )
                        return
            if (self.documents_collected==3 and not self.evaluation_started and not self.evaluation_finished and
                self.player.rect.colliderect(station.inflate(50,50))):
                self.start_evaluation(); return
            if (
                self.current_office=="B"
                and self.b_exit_unlocked
                and self.b_insane_active
                and self.player.rect.colliderect(exit_rect.inflate(60,60))
            ):
                self.b_insane_active = False
                self.b_exit_unlocked = False

                self.boss_active = False
                self.boss.active = False
                self.boss.chasing = False
                self.boss_state = "idle"

                # Escapar não encerra a Fase 1.
                self.office_b_passed = True
                self.phase1_return_pending = True

                self.current_room = "office"
                self.current_office = "B"
                self.player.rect.topleft = (760,400)

                self.objective = "Voltar para a recepcao e falar com Clara"
                self.escape_transition_timer = self.escape_transition_duration
                self.dialogue.show("Voce escapou do chefe.")
                self.mission_ui.show(
                    "ESCAPOU",
                    "Volte para a recepcao e fale com Clara."
                )
                return

            # EXAMINAR OBJETOS
            if not self.evaluation_started and not self.evaluation_finished:
                exam_names = ("relogio_a", "computador_a") if self.current_office == "A" else ("relogio_b", "monitor_b")
                for exam_name in exam_names:
                    obj = self.exam_objects[exam_name]
                    if self.player.rect.colliderect(obj["rect"].inflate(55, 55)):
                        if exam_name == "monitor_b" and self.b_tension >= 60:
                            self.dialogue.show("O monitor esta ligado. Agora ha um arquivo aberto, mas voce nao lembra de ter aberto nada.")
                        else:
                            self.dialogue.show(obj["text"])
                        return

            if self.evaluation_finished and self.player.rect.colliderect(exit_rect.inflate(40,40)):
                if self.current_office=="A":
                    self.office_a_passed=True; self.office_b_unlocked=True; self.current_room="office"
                    self.player.rect.topleft=(760,400); self.objective="Ir ate a porta do Escritorio B"
                    self.dialogue.show("Voce concluiu o Escritorio A. Volte para a recepcao.")
                    self.mission_ui.show("NOVA ETAPA","Entre no Escritorio B")
                else:
                    self.office_b_passed = True
                    self.phase1_return_pending = True
                    self.current_room = "office"
                    self.current_office = "B"
                    self.player.rect.topleft = (760,400)
                    self.objective = "Voltar para a recepcao e falar com Clara"
                    self.dialogue.show("Volte para a recepcao.")
                    self.mission_ui.show(
                        "RETORNO",
                        "Fale com Clara para finalizar a Fase 1."
                    )

    def enter_office(self, office):
        self.current_office=office; self.current_room="office_a" if office=="A" else "office_b"
        self.office_obstacles=self.office_a_obstacles if office=="A" else self.office_b_obstacles
        self.player.rect.topleft=(150,500); self.documents_collected=0
        for doc in self.get_current_documents(): doc.collected=False
        self.math=MathChallenge(); self.evaluation_started=False; self.evaluation_has_started=False
        self.evaluation_finished=False; self.evaluation_intro_timer=0.0; self.escape_transition_timer=0.0; self.recovery_mode=False; self.b_insane_active=False; self.b_exit_unlocked=False; self.dialogue.hide()
        self.boss_active=False; self.boss.active=False; self.boss_state="idle"; self.boss.chasing=False
        self.boss.rect.topleft=(1050,180); self.boss_path=[]; self.boss_path_target=None; self.boss_roam_target=None
        self.boss_stuck_timer=0.0; self.boss_last_position=pygame.Vector2(self.boss.rect.center)
        self.b_tension=0.0; self.b_tension_max=100.0; self.b_tension_stage=0
        self.b_corruption_anim_timer=0.0
        self.b_ambient_event_timer=0.0; self.b_ambient_event_cooldown=10.0; self.b_ambient_event_active=False; self.b_ambient_event_shift=0; self.b_ambient_event_type=0
        self.objective="Encontrar os documentos"; self.mission_ui.show("ESCRITORIO "+office,"Encontre os 3 documentos")
    def get_current_documents(self):
        return self.a_documents if self.current_office=="A" else self.b_documents
    def get_current_station(self):
        return self.math_station if self.current_office=="A" else self.b_math_station
    def get_current_exit(self):
        return self.office_a_exit if self.current_office=="A" else self.office_b_exit

    # =====================================================
    # INICIAR AVALIAÇÃO
    # =====================================================

    # =====================================================
    # CONFIGURAR QUESTOES POR ESCRITORIO / RECUPERACAO
    # =====================================================

    def configure_math_questions(self):

        normal_a = [
            {"question": "Quanto e 8 + 7?", "answers": ["12", "15", "16", "14"], "correct": 1},
            {"question": "Quanto e 9 x 6?", "answers": ["54", "48", "56", "63"], "correct": 0},
            {"question": "Quanto e 72 / 8?", "answers": ["8", "9", "10", "7"], "correct": 1},
            {"question": "Quanto e 15 - 8?", "answers": ["6", "8", "7", "9"], "correct": 2},
            {"question": "Quanto e 12 x 4?", "answers": ["36", "48", "44", "52"], "correct": 1},
        ]

        normal_b = [
            {"question": "Quanto e 17 x 6?", "answers": ["92", "102", "112", "96"], "correct": 1},
            {"question": "Quanto e 144 / 12?", "answers": ["10", "11", "12", "14"], "correct": 2},
            {"question": "Quanto e 25% de 80?", "answers": ["15", "20", "25", "30"], "correct": 1},
            {"question": "Quanto e 18 + 7 x 2?", "answers": ["50", "32", "40", "25"], "correct": 1},
            {"question": "Quanto e 15 ao quadrado?", "answers": ["125", "200", "225", "250"], "correct": 2},
        ]

        recovery_a = [
            {"question": "Quanto e 27 x 14?", "answers": ["368", "378", "388", "398"], "correct": 1},
            {"question": "Quanto e 432 / 18?", "answers": ["22", "24", "26", "28"], "correct": 1},
            {"question": "Quanto e 35% de 240?", "answers": ["72", "78", "84", "90"], "correct": 2},
            {"question": "Quanto e 12 ao quadrado - 5 ao quadrado?", "answers": ["109", "119", "129", "139"], "correct": 1},
            {"question": "Quanto e (84 / 7) x 6?", "answers": ["66", "72", "78", "84"], "correct": 1},
        ]

        recovery_b = [
            {"question": "Quanto e 24 x 17?", "answers": ["398", "408", "418", "428"], "correct": 1},
            {"question": "Quanto e 672 / 21?", "answers": ["28", "30", "32", "34"], "correct": 2},
            {"question": "Quanto e 18% de 250?", "answers": ["35", "40", "45", "50"], "correct": 2},
            {"question": "Quanto e 5 ao cubo - 3 ao quadrado?", "answers": ["106", "116", "126", "136"], "correct": 1},
            {"question": "Quanto e (320 - 80) / 12?", "answers": ["18", "20", "22", "24"], "correct": 1},
        ]

        if self.current_office == "B":
            questions = recovery_b if self.recovery_mode else normal_b
        else:
            questions = recovery_a if self.recovery_mode else normal_a

        self.math.questions = questions

    def generate_b_question(self):
        self.b_question_number += 1
        level = min(4, (self.b_question_number - 1) // 2)
        self.b_corruption_level = level
        a = random.randint(8 + level * 4, 25 + level * 12)
        b = random.randint(2 + level, 9 + level * 2)
        op = random.choice(["+", "-", "x", "/"])
        if op == "+": answer = a + b
        elif op == "-":
            if b > a: a, b = b, a
            answer = a - b
        elif op == "x": answer = a * b
        else:
            b = random.randint(2, 9); a = b * random.randint(2 + level, 10 + level); answer = a // b
        answers=[answer]
        while len(answers)<4:
            c=answer+random.choice([-3,-2,-1,1,2,3,5,7])
            if c not in answers: answers.append(c)
        random.shuffle(answers)
        q=f"Quanto e {a} {op} {b}?"
        if level==1: q=q.replace("Quanto","QU4NT0")
        elif level==2: q=q.replace("Quanto","QU4NT0").replace("e","3",1); q=q.replace(str(a),str(a)[0]+"█",1)
        elif level==3: q=f"QU4NT0 E {str(a)[0]}█ {op} █?"
        elif level>=4: q=random.choice(["R3SP0ND4.","█3SP0ND4.","ERR0R // R3SP0ND4",f"{str(a)[0]}█ {op} █ = ?"])
        return {"question":q,"answers":[str(x) for x in answers],"correct":answers.index(answer)}

    def start_b_corrupted_evaluation(self):
        self.evaluation_started=True; self.evaluation_has_started=True; self.evaluation_finished=False
        self.b_question_number=0; self.b_corruption_level=0; self.b_question_answered=False; self.b_evaluation_complete=False
        self.b_corruption_anim_timer=0.0
        self.b_boss_reveal_pending = False
        self.b_boss_reveal_timer = 0.0

        # O Escritório B também usa a transição antes de abrir a avaliação.
        # Assim a interface corrompida não aparece de repente.
        self.math.active = False
        self.evaluation_intro_timer = self.evaluation_intro_duration
        self.math.active=False; self.math.finished=False; self.math.current_question=0; self.math.correct_answers=0; self.math.wrong_answers=0
        # O Escritório B tem 10 questões; a corrupção aumenta conforme a questão avança.
        self.math.questions=[self.generate_b_question() for _ in range(10)]
        self.objective="Responda a avaliacao corrompida"
        self.mission_ui.show("ESCRITORIO B","Algo esta errado com esta avaliacao...")

    def answer_b_corrupted(self, answer_index):
        q=self.math.questions[0]
        if answer_index == q["correct"]:
            self.math.correct_answers += 1; self.dialogue.show("Resposta correta... mas algo continua errado.")
        else:
            self.math.wrong_answers += 1; self.dialogue.show("Resposta registrada. O chefe ficou irritado.")
        self.b_question_answered=True; self.anger=min(self.max_anger,self.anger+1)
        if self.anger==2 and not self.boss_active:
            self.boss_active=True; self.boss.activate(); self.boss_state="patrol"; self.boss_roam_target=None; self.boss_roam_wait=0.0; self.boss_search_timer=0; self.boss_last_seen=None; self.boss_lost_sight_timer=0.0; self.mission_ui.show("ALERTA","O chefe percebeu alguma coisa...")
        if self.anger==3:
            self.boss_state="search"; self.boss_search_timer=0.0; self.boss_last_seen=self.player.rect.center
        if self.anger==4:
            self.boss_state="chase"; self.boss.chasing=True; self.boss.speed=2.15; self.mission_ui.show("PERIGO","Continue. Nao pare agora.")
        if self.anger>=self.max_anger:
            self.boss_state="insane"; self.boss.chasing=True; self.boss.speed=3.0; self.b_insane_active=True; self.b_exit_unlocked=False; self.evaluation_started=False; self.b_evaluation_complete=True; self.math.active=False; self.evaluation_finished=False; self.objective="FUJA! O chefe perdeu o controle."; self.mission_ui.show("MODO INSANO","O chefe perdeu o controle!"); self.dialogue.show("CHEGA."); return
        self.math.questions=[self.generate_b_question()]; self.math.current_question=0; self.b_question_answered=False

    def start_evaluation(self):
        if self.current_office == "B":
            self.start_b_corrupted_evaluation()
            return


        first_open = not self.evaluation_has_started

        # Primeira abertura: cria/inicia a avaliação.
        if first_open:
            # Inicia o desafio e, logo depois, força o banco correto.
            # Isso evita que MathChallenge.start() restaure as questões normais.
            self.math.start()
            self.configure_math_questions()
            self.evaluation_has_started = True

        # Aberturas seguintes: apenas retoma a avaliação.
        # Não chamamos math.start() novamente para não perder o progresso.
        self.math.active = False
        self.evaluation_started = True
        self.evaluation_intro_timer = self.evaluation_intro_duration

        self.objective = (
            "Responder a avaliacao"
        )

        self.mission_ui.show(
            "AVALIACAO",
            "Responda as questoes" if first_open else "Continuar avaliacao"
        )

    # =====================================================
    # RESPONDER QUESTÃO
    # =====================================================

    def answer_question(self, answer_index):

        result = self.math.answer(
            answer_index
        )

        if result:
            self.dialogue.show(
                "Resposta correta!"
            )
        else:
            self.dialogue.show(
                "Resposta errada!"
            )

        # ESCRITORIO B: toda resposta aumenta a tensao.
        # Acerto = +10 | Erro = +14.
        # A mensagem tambem muda o clima, mesmo quando o jogador acerta.
        if self.current_office == "B":
            self.add_b_tension(10 if result else 14)

            if result:
                tension_messages = [
                    "Resposta correta... mas o ambiente parece mais estranho.",
                    "Correto. Por que a sensacao de que algo esta errado aumentou?",
                    "Resposta registrada. O silencio ficou ainda mais pesado.",
                    "Correto... alguma coisa nao parece estar certa.",
                ]
            else:
                tension_messages = [
                    "Resposta errada. Voce sente que alguem esta observando.",
                    "Resposta registrada... e alguma coisa mudou.",
                    "Errado. O ambiente parece reagir a sua resposta.",
                    "Resposta errada... voce ouviu alguma coisa?",
                ]

            message_index = (
                self.b_question_number
                + self.math.wrong_answers
                + self.math.correct_answers
            ) % len(tension_messages)

            self.dialogue.show(
                tension_messages[message_index]
            )

        # -------------------------
        # AVALIAÇÃO TERMINOU
        # -------------------------
        if self.math.finished:
            self.evaluation_started = False

            # Escritório B: somente depois das 10 questoes a tensao
            # libera a escalada do chefe.
            if self.current_office == "B":
                if self.b_tension >= self.b_tension_max:
                    # A prova terminou. O chefe ainda NÃO aparece.
                    # Primeiro vem uma pequena pausa de suspense para a
                    # pessoa da feira perceber que alguma coisa mudou.
                    self.b_boss_reveal_pending = True
                    self.b_boss_reveal_timer = self.b_boss_reveal_duration
                    self.boss_active = False
                    self.boss.active = False
                    self.boss_state = "idle"
                    self.b_insane_active = False
                    self.b_exit_unlocked = False
                    self.evaluation_finished = True
                    self.objective = "..."
                    self.mission_ui.show(
                        "AVALIACAO CONCLUIDA",
                        "..."
                    )
                    self.dialogue.show(
                        "..."
                    )
                    return
                else:
                    self.evaluation_finished = True
                    self.objective = "Ir ate a saida do escritorio"
                    self.mission_ui.show("AVALIACAO CONCLUIDA", "Algo esta errado aqui... Va ate a saida.")
                    return

            # 3 ou mais erros: recuperacao. Isso vale para A e B.
            if self.math.wrong_answers >= 3 and not self.recovery_mode:
                self.recovery_mode = True
                self.evaluation_has_started = False
                self.evaluation_finished = False
                self.math = MathChallenge()
                self.dialogue.show("Voce foi mal. Sera necessario fazer a recuperacao.")
                self.mission_ui.show("RECUPERACAO", "Questoes diferentes e mais dificeis.")
                self.objective = "Fazer a avaliacao de recuperacao"
                return

            # Se falhar na recuperacao, permite refazer a recuperacao.
            if self.recovery_mode and self.math.wrong_answers >= 3:
                self.evaluation_has_started = False
                self.evaluation_finished = False
                self.math = MathChallenge()
                self.dialogue.show("A recuperacao nao foi suficiente. Tente novamente.")
                self.mission_ui.show("RECUPERACAO", "Refaca a recuperacao com questoes diferentes.")
                self.objective = "Refazer a recuperacao"
                return

            self.evaluation_finished = True
            self.objective = "Ir ate a saida do escritorio"
            self.mission_ui.show("AVALIACAO CONCLUIDA", "Va ate a saida do escritorio")

            # V58: pequeno sinal de suspense depois da avaliacao do Escritorio A.
            # A mensagem e apenas narrativa: nao altera objetivos nem mecanicas.
            if self.current_office == "A" and not self.recovery_mode:
                self.dialogue.show(
                    "A avaliacao foi registrada. Por um instante, a tela mostra uma linha estranha... e ela desaparece."
                )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, dt):

        if self.escape_transition_timer > 0:
            self.escape_transition_timer -= dt
            if self.escape_transition_timer < 0:
                self.escape_transition_timer = 0.0

        if self.victory:
            self.phase1_ending_timer = min(
                self.phase1_ending_duration,
                self.phase1_ending_timer + dt
            )

        if self.evaluation_intro_timer > 0:
            self.evaluation_intro_timer -= dt
            if self.evaluation_intro_timer <= 0:
                self.evaluation_intro_timer = 0.0
                self.math.active = True

        # Evento raro no Escritório B: uma folha se desloca levemente por um instante.
        if self.current_office == "B" and not self.math.active and not self.victory and not self.game_over:
            self.b_ambient_event_cooldown -= dt
            if self.b_ambient_event_active:
                self.b_ambient_event_timer -= dt
                if self.b_ambient_event_timer <= 0:
                    self.b_ambient_event_active = False
                    self.b_ambient_event_cooldown = 9.0
                    self.b_ambient_event_shift = 0
                    self.b_ambient_event_type = 0
            elif self.b_ambient_event_cooldown <= 0:
                self.b_ambient_event_active = True
                self.b_ambient_event_timer = self.b_ambient_event_duration
                self.b_ambient_event_type = random.randint(0, 2)
                self.b_ambient_event_shift = 4

        if self.current_office == "B" and self.math.active:
            self.b_corruption_anim_timer += dt

        # ----------------------------------------------------
        # REVELAÇÃO DO CHEFE — após a avaliação
        # ----------------------------------------------------
        if (
            self.current_office == "B"
            and self.b_boss_reveal_pending
            and not self.game_over
            and not self.victory
        ):
            self.b_boss_reveal_timer -= dt

            if self.b_boss_reveal_timer <= 0:
                self.b_boss_reveal_pending = False

                self.boss_active = True
                self.boss.activate()
                self.boss_state = "insane"
                self.boss.chasing = True
                self.boss.speed = 4.2
                self.boss_stuck_timer = 0.0
                self.boss_last_position = pygame.Vector2(
                    self.boss.rect.center
                )
                self.b_insane_active = True
                self.b_exit_unlocked = True

                self.objective = "ESCAPE! O chefe ficou INSANO!"
                self.mission_ui.show(
                    "MODO INSANO",
                    "Fuja do chefe! Encontre a saida."
                )
                self.dialogue.show(
                    "ALGUMA COISA MUDOU."
                )

        # =========================
        # MOVIMENTO DO JOGADOR
        # =========================

        if self.current_room == "office":

            self.player.update(
                self.map.walls,
                dt
            )

            self.camera.update(
                self.player.rect
            )

        elif self.current_room in ("office_a", "office_b"):

            self.player.update(
                self.office_obstacles,
                dt
            )

            # Mantém o jogador dentro da área visível.
            # Mesmo limite físico usado pelo chefe.
            self.player.rect.clamp_ip(
                self.get_office_room_bounds()
            )

            self.camera.offset_x = 0
            self.camera.offset_y = 0

        # =========================
        # CHECKPOINT
        # =========================

        if self.checkpoint_active:

            self.checkpoint_timer += dt

            if self.checkpoint_timer >= self.checkpoint_duration:
                self.reset_office_checkpoint()

        # =========================
        # CHEFE
        # =========================

        if (
            self.current_room in ("office_a", "office_b")
            and self.boss_active
            and not self.math.active
            and not self.game_over
            and not self.victory
            and not self.checkpoint_active
        ):

            self.update_boss_ai(dt)

            if self.boss.rect.colliderect(
                self.player.rect
            ):

                self.game_over = True
                self.checkpoint_active = True
                self.checkpoint_timer = 0

                self.dialogue.show(
                    "Voce foi pego!"
                )

                checkpoint_name = "B" if self.current_office == "B" else "A"
                self.mission_ui.show(
                    "CHECKPOINT",
                    f"Voltando ao inicio do Escritorio {checkpoint_name}..."
                )

        # =========================
        # INTERFACES
        # =========================

        self.dialogue.update(dt)
        self.mission_ui.update(dt)

        # Sempre limpa o prompt antes de procurar uma nova interação.
        self.interaction_text = ""
        self.interaction_rect = None

        # =========================
        # INTERAÇÕES - RECEPÇÃO
        # =========================

        if self.current_room == "office":

            if self.player.rect.colliderect(
                self.clara.rect.inflate(80, 80)
            ):
                self.interaction_text = (
                    "[E] Finalizar Fase 1"
                    if self.phase1_return_pending
                    else "[E] Falar"
                )
                self.interaction_rect = self.clara.rect

            elif (
                self.talked_to_clara
                and not self.badge.collected
                and self.player.rect.colliderect(
                    self.badge.rect.inflate(80, 80)
                )
            ):
                self.interaction_text = "[E] Pegar"
                self.interaction_rect = self.badge.rect

            elif (
                self.has_badge
                and self.player.rect.colliderect(
                    self.office_door.rect.inflate(80, 80)
                )
            ):
                self.interaction_text = "[E] Entrar"
                self.interaction_rect = self.office_door.rect

            elif self.office_b_unlocked and self.player.rect.colliderect(
                self.office_b_door.rect.inflate(80,80)
                ):
                self.interaction_text="[E] Entrar no B"
                self.interaction_rect=self.office_b_door.rect

        # =========================
        # INTERAÇÕES - ESCRITÓRIO A
        # =========================

        elif self.current_room in ("office_a", "office_b"):
            documents = self.get_current_documents(); station=self.get_current_station(); exit_rect=self.get_current_exit()
            # Documentos só ficam interativos antes da avaliação.
            if not self.evaluation_started and self.documents_collected < 3:
                for doc in documents:
                    if (
                        not doc.collected
                        and self.player.rect.colliderect(
                            doc.rect.inflate(60, 60)
                        )
                    ):
                        self.interaction_text = "[E] Pegar"
                        self.interaction_rect = doc.rect
                        break

            # Estação só fica interativa depois dos 3 documentos.
            if (
                self.documents_collected == 3
                and not self.evaluation_started
                and not self.evaluation_finished
                and self.player.rect.colliderect(
                    station.inflate(60, 60)
                )
            ):
                if self.evaluation_has_started:
                    self.interaction_text = "[E] Continuar avaliação"
                else:
                    self.interaction_text = "[E] Iniciar avaliação"

                self.interaction_rect = station

            # Saída só fica interativa depois de terminar a avaliação.
            elif (
                self.current_office == "A"
                and self.evaluation_finished
                and not self.victory
                and self.player.rect.colliderect(
                    exit_rect.inflate(60, 60)
                )
            ):
                self.interaction_text = "[E] Sair"
                self.interaction_rect = exit_rect

            if not self.interaction_text and not self.evaluation_started and not self.evaluation_finished:
                exam_names = ("relogio_a", "computador_a") if self.current_office == "A" else ("relogio_b", "monitor_b")
                for exam_name in exam_names:
                    obj = self.exam_objects[exam_name]
                    if self.player.rect.colliderect(obj["rect"].inflate(55, 55)):
                        self.interaction_text = "[E] Examinar"
                        self.interaction_rect = obj["rect"]
                        break

    # =====================================================
    # DRAW
    # =====================================================

    def draw(self):

        self.screen.fill(
            (35, 35, 35)
        )

        # =========================
        # SALA PRINCIPAL
        # =========================

        if self.current_room == "office":

            self.draw_office()

        # =========================
        # ESCRITÓRIO A
        # =========================

        elif self.current_room in ("office_a", "office_b"):

            self.draw_office_a()

        # =========================
        # INTERFACE
        # =========================

        self.dialogue.draw(
            self.screen
        )

        self.mission_ui.draw(
            self.screen
        )

        # =========================
        # REVELAÇÃO CINEMÁTICA DO CHEFE
        # =========================
        if (
            self.current_office == "B"
            and self.b_boss_reveal_pending
        ):
            remaining = self.b_boss_reveal_timer
            progress = 1.0 - (remaining / self.b_boss_reveal_duration)

            # Escurece o ambiente gradualmente, sem esconder totalmente o mapa.
            reveal_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(25 + 55 * max(0.0, min(1.0, progress)))
            reveal_overlay.fill((0, 0, 0, alpha))
            self.screen.blit(reveal_overlay, (0, 0))

            # O texto só aparece na parte final da contagem.
            if remaining <= 1.4:
                reveal_text = self.big_font.render(
                    "ALGUMA COISA MUDOU.",
                    True,
                    WHITE
                )
                self.screen.blit(
                    reveal_text,
                    (
                        WIDTH // 2 - reveal_text.get_width() // 2,
                        HEIGHT // 2 - reveal_text.get_height() // 2
                    )
                )

        # =========================
        # INDICADOR DE INTERAÇÃO
        # =========================

        if self.interaction_text and self.interaction_rect is not None:

            txt = self.font.render(
                self.interaction_text,
                True,
                WHITE
            )

            if self.current_room == "office":

                pos = self.camera.apply_rect(
                    self.interaction_rect
                )
            else:
                pos = self.interaction_rect

            # Destaca discretamente o objeto que pode ser usado/examinado.
            if self.interaction_text == "[E] Examinar":
                pulse = 90 + int(35 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 260.0)))
                pygame.draw.rect(
                    self.screen,
                    (pulse, pulse, 120),
                    pos.inflate(8, 8),
                    2,
                    border_radius=5
                )

            # Caixa escura pequena deixa o comando legível sobre o cenário.
            prompt_rect = txt.get_rect(
                centerx=pos.centerx,
                bottom=pos.top - 8
            ).inflate(18, 10)
            pygame.draw.rect(
                self.screen,
                (18, 18, 20),
                prompt_rect,
                border_radius=6
            )
            pygame.draw.rect(
                self.screen,
                (95, 95, 100),
                prompt_rect,
                1,
                border_radius=6
            )

            self.screen.blit(
                txt,
                (
                    prompt_rect.centerx - txt.get_width() // 2,
                    prompt_rect.centery - txt.get_height() // 2
                )
            )

        # =========================
        # TRANSIÇÃO DA AVALIAÇÃO
        # =========================

        if self.evaluation_intro_timer > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 125))
            self.screen.blit(overlay, (0, 0))

            progress = 1.0 - (self.evaluation_intro_timer / self.evaluation_intro_duration)
            panel_w = 620
            panel_h = 150
            panel_x = WIDTH // 2 - panel_w // 2
            panel_y = HEIGHT // 2 - panel_h // 2

            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel.fill((10, 10, 12, 215))
            pygame.draw.rect(panel, (90, 90, 95, 220), panel.get_rect(), 2, border_radius=8)
            self.screen.blit(panel, (panel_x, panel_y))

            intro_title_text = (
                "ACESSANDO AVALIAÇÃO CORROMPIDA..."
                if self.current_office == "B"
                else "ACESSANDO AVALIAÇÃO..."
            )

            intro_title = self.big_font.render(
                intro_title_text,
                True,
                WHITE
            )
            self.screen.blit(
                intro_title,
                (WIDTH // 2 - intro_title.get_width() // 2, panel_y + 28)
            )

            bar_rect = pygame.Rect(panel_x + 70, panel_y + 92, panel_w - 140, 12)
            pygame.draw.rect(self.screen, (65, 65, 70), bar_rect, border_radius=6)
            fill_rect = bar_rect.copy()
            fill_rect.width = int(bar_rect.width * max(0.0, min(1.0, progress)))
            if fill_rect.width > 0:
                pygame.draw.rect(self.screen, (190, 190, 195), fill_rect, border_radius=6)

        # =========================
        # AVALIAÇÃO
        # =========================

        if self.math.active:

            self.draw_math_question()

        # =========================
        # TRANSICAO APOS ESCAPAR
        # =========================
        if self.escape_transition_timer > 0:
            progress = max(0.0, min(1.0, self.escape_transition_timer / self.escape_transition_duration))
            alpha = int(185 * progress)
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            self.screen.blit(overlay, (0, 0))

            title = self.big_font.render("VOCE ESCAPOU", True, WHITE)
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80)
            )

            sub = self.font.render(
                "Volte para a recepcao.",
                True,
                WHITE
            )
            self.screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2 - 28)
            )

        # =========================
        # VITÓRIA
        # =========================

        if self.victory:

            self.draw_victory()

        if self.game_over:

            self.draw_game_over()

        pygame.display.flip()

    # =====================================================
    # DESENHAR SALA PRINCIPAL
    # =====================================================

    def draw_office(self):

        self.map.draw(
            self.screen,
            self.camera
        )

        self.clara.draw(
            self.screen,
            self.camera
        )

        self.badge.draw(
            self.screen,
            self.camera
        )

        self.office_door.draw(
            self.screen,
            self.camera
        )

        self.office_b_door.draw(self.screen, self.camera)

        label_a = self.big_font.render("A", True, WHITE)
        label_b = self.big_font.render("B", True, WHITE)
        a_pos = self.camera.apply_rect(self.office_door.rect)
        b_pos = self.camera.apply_rect(self.office_b_door.rect)
        self.screen.blit(label_a, (a_pos.centerx-label_a.get_width()//2, a_pos.top-45))
        if self.office_b_unlocked:
            self.screen.blit(label_b, (b_pos.centerx-label_b.get_width()//2, b_pos.top-45))
        else:
            locked = self.font.render("B BLOQUEADO", True, (180,180,180))
            self.screen.blit(locked, (b_pos.centerx-locked.get_width()//2, b_pos.top-40))

        self.player.draw(
            self.screen,
            self.camera
        )

        # -------------------------
        # ESTAMINA
        # -------------------------

        pygame.draw.rect(
            self.screen,
            RED,
            (20, 20, 200, 20)
        )

        pygame.draw.rect(
            self.screen,
            GREEN,
            (
                20,
                20,
                200 * (
                    self.player.stamina /
                    MAX_STAMINA
                ),
                20
            )
        )

        stamina_text = self.font.render(
            f"Estamina: {int(self.player.stamina)}",
            True,
            WHITE
        )

        self.screen.blit(
            stamina_text,
            (20, 50)
        )

        # -------------------------
        # OBJETIVO
        # -------------------------

        objective_text = self.font.render(
            f"Objetivo: {self.objective}",
            True,
            WHITE
        )

        self.screen.blit(
            objective_text,
            (850, 20)
        )

    # =====================================================
    # DESENHAR ESCRITÓRIO A
    # =====================================================

    def draw_office_a(self):

        self.screen.fill(
            (70, 70, 100)
        )

        # -------------------------
        # PISO
        # -------------------------

        pygame.draw.rect(
            self.screen,
            (120, 70, 40),
            (100, 100, 1080, 520)
        )

        # -------------------------
        # ILUMINAÇÃO / IDENTIDADE VISUAL
        # -------------------------
        # Detalhes puramente visuais para diferenciar A de B.
        # Nenhum deles interfere em colisao, avaliacao ou IA.
        wall_panel_color = (92, 57, 36) if self.current_office == "A" else (82, 58, 43)
        pygame.draw.rect(self.screen, wall_panel_color, (125, 115, 1030, 20))
        pygame.draw.rect(self.screen, (42, 32, 26), (125, 115, 1030, 20), 2)

        lamp_positions = [245, 475, 705, 935]
        for lamp_x in lamp_positions:
            lamp_color = (185, 178, 150)
            lamp_alpha_rect = pygame.Rect(lamp_x, 102, 120, 8)

            # No B, a luz pode falhar lentamente conforme a tensao sobe.
            if self.current_office == "B" and self.b_tension >= 40:
                flicker_tick = (pygame.time.get_ticks() // 650 + lamp_x // 115) % 4
                if flicker_tick == 0:
                    lamp_color = (75, 72, 65)
                elif flicker_tick == 1 and self.b_tension >= 80:
                    lamp_color = (35, 34, 33)

            pygame.draw.rect(self.screen, (38, 34, 29), (lamp_x, 100, 120, 12))
            pygame.draw.rect(self.screen, lamp_color, lamp_alpha_rect)

        # Pequena placa da sala. A fica organizada; B parece levemente deslocada.
        sign_rect = pygame.Rect(110, 145, 140, 28)
        pygame.draw.rect(self.screen, (53, 48, 42), sign_rect)
        pygame.draw.rect(self.screen, (132, 126, 112), sign_rect, 1)
        sign_font = pygame.font.SysFont(None, 14)
        sign_text = sign_font.render(
            "SETOR A" if self.current_office == "A" else "SETOR B",
            True,
            (215, 210, 195)
        )
        sign_x = sign_rect.x + 10
        sign_y = sign_rect.y + 7
        if self.current_office == "B":
            sign_x += 1
            sign_y += 1
        self.screen.blit(sign_text, (sign_x, sign_y))

        # -------------------------
        # TÍTULO
        # -------------------------

        title = self.font.render(
            f"ESCRITORIO {self.current_office}",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (520, 40)
        )

        # -------------------------
        # OBJETIVO
        # -------------------------

        objective_text = self.font.render(
            f"Objetivo: {self.objective}",
            True,
            WHITE
        )

        self.screen.blit(
            objective_text,
            (850, 20)
        )

        # -------------------------
        # OBSTÁCULOS / MÓVEIS
        # -------------------------
        # Os mesmos retângulos usados pela colisão/IA também são
        # desenhados aqui, para ficarem visíveis durante a avaliação.
        for obstacle in self.office_obstacles:
            pygame.draw.rect(self.screen, (75, 43, 27), obstacle)
            pygame.draw.rect(self.screen, (35, 22, 14), obstacle, 5)

            inner = obstacle.inflate(-10, -10)
            if inner.width > 0 and inner.height > 0:
                pygame.draw.rect(self.screen, (105, 61, 36), inner, 3)

        # Pequenos detalhes fisicos do ambiente.
        clock_rect = self.exam_objects["relogio_a"]["rect"] if self.current_office == "A" else self.exam_objects["relogio_b"]["rect"]
        pygame.draw.rect(self.screen, (48, 43, 37), clock_rect)
        pygame.draw.rect(self.screen, (150, 145, 132), clock_rect.inflate(-4, -4), 1)
        pygame.draw.line(self.screen, (70, 66, 59), clock_rect.center, (clock_rect.centerx, clock_rect.y + 8), 1)
        pygame.draw.line(self.screen, (70, 66, 59), clock_rect.center, (clock_rect.right - 8, clock_rect.centery), 1)

        trash_x = 990 if self.current_office == "B" else 940
        pygame.draw.rect(self.screen, (50, 44, 37), (trash_x, 500, 28, 34))
        pygame.draw.rect(self.screen, (30, 27, 23), (trash_x - 2, 496, 32, 6))

        # -------------------------
        # DETALHES DE ESCRITÓRIO — ESCRITÓRIO A
        # -------------------------
        # O Escritório A permanece visualmente mais normal e organizado.
        # Estes elementos são apenas decorativos e não alteram a jogabilidade.
        if self.current_office == "A":
            paper_font_a = pygame.font.SysFont(None, 9)

            def draw_paper_a(rect, heading, line_count=3):
                paper = pygame.Rect(rect)
                pygame.draw.rect(self.screen, (224, 218, 199), paper)
                pygame.draw.rect(self.screen, (135, 128, 111), paper, 1)

                heading_text = paper_font_a.render(heading, True, (58, 54, 47))
                self.screen.blit(heading_text, (paper.x + 2, paper.y + 2))

                for line_index in range(line_count):
                    y_line = paper.y + 9 + line_index * 4
                    pygame.draw.line(
                        self.screen,
                        (75, 70, 62),
                        (paper.x + 2, y_line),
                        (paper.right - 2, y_line),
                        1
                    )

            draw_paper_a((205, 280, 34, 22), "RELATORIO", 3)
            draw_paper_a((725, 283, 30, 20), "TAREFA", 2)
            draw_paper_a((425, 493, 28, 20), "NOTA", 2)

            # Computador discreto sobre a mesa superior do A.
            monitor_a = self.exam_objects["computador_a"]["rect"]
            pygame.draw.rect(self.screen, (28, 24, 21), monitor_a.inflate(10, 8))
            pygame.draw.rect(self.screen, (15, 16, 18), monitor_a, border_radius=2)
            pygame.draw.rect(self.screen, (25, 28, 30), monitor_a.inflate(-7, -7))
            pygame.draw.rect(self.screen, (28, 24, 20), (monitor_a.centerx - 5, monitor_a.bottom, 10, 8))
            pygame.draw.rect(self.screen, (45, 38, 30), (monitor_a.centerx - 18, monitor_a.bottom + 8, 36, 5))

            # Pequeno porta-canetas sobre a mesa superior.
            pygame.draw.rect(self.screen, (48, 39, 31), (820, 286, 12, 13))
            pygame.draw.rect(self.screen, (90, 76, 59), (822, 280, 2, 8))
            pygame.draw.rect(self.screen, (75, 63, 50), (826, 278, 2, 10))

            # Cadeira alinhada à mesa inferior.
            pygame.draw.rect(self.screen, (45, 31, 24), (785, 575, 34, 26))
            pygame.draw.rect(self.screen, (25, 20, 17), (789, 569, 26, 10))
            pygame.draw.rect(self.screen, (35, 27, 21), (797, 601, 7, 16))

        # -------------------------
        # SINAIS SUTIS — ESCRITÓRIO B
        # -------------------------
        # Pequenos detalhes visuais aparecem antes da avaliacao,
        # sem alterar a jogabilidade ou acelerar a tensao.
        if self.current_office == "B":
            flicker_phase = (pygame.time.get_ticks() // 900) % 2

            # Computador menor, apoiado sobre a mesa superior.
            # A tela e o suporte ficam dentro da area da mesa, sem parecer flutuar.
            monitor = pygame.Rect(742, 225, 68, 40)
            pygame.draw.rect(self.screen, (28, 23, 19), monitor.inflate(10, 8))
            pygame.draw.rect(self.screen, (15, 16, 18), monitor, border_radius=2)

            if self.b_tension >= 20:
                screen_color = (150, 150, 125) if flicker_phase == 0 else (35, 40, 42)
            else:
                screen_color = (25, 28, 30)

            pygame.draw.rect(self.screen, screen_color, monitor.inflate(-7, -7))

            # Eventos raros e muito sutis: o escritorio parece mudar por um instante.
            if self.b_ambient_event_active:
                if self.b_ambient_event_type == 0:
                    # Uma folha parece ter sido movida.
                    event_paper = pygame.Rect(680 + self.b_ambient_event_shift, 255, 30, 21)
                    pygame.draw.rect(self.screen, (224, 218, 199), event_paper)
                    pygame.draw.rect(self.screen, (135, 128, 111), event_paper, 1)
                    pygame.draw.line(self.screen, (58, 54, 47), (event_paper.x + 2, event_paper.y + 12), (event_paper.right - 2, event_paper.y + 12), 1)
                    pygame.draw.line(self.screen, (58, 54, 47), (event_paper.x + 2, event_paper.y + 16), (event_paper.right - 5, event_paper.y + 16), 1)

                elif self.b_ambient_event_type == 1:
                    # O monitor pisca um pequeno indicador, sem alterar seu estado principal.
                    pygame.draw.rect(self.screen, (180, 175, 150), (790, 269, 3, 3))
                    pygame.draw.line(self.screen, (125, 125, 108), (775, 260), (803, 260), 1)

                else:
                    # A cadeira parece um pouco fora da posição por um instante.
                    chair_shift = self.b_ambient_event_shift
                    pygame.draw.rect(self.screen, (45, 31, 24), (750 + chair_shift, 301, 34, 26))
                    pygame.draw.rect(self.screen, (25, 20, 17), (754 + chair_shift, 295, 26, 10))
                    pygame.draw.rect(self.screen, (35, 27, 21), (762 + chair_shift, 327, 7, 16))

            # O monitor comeca a exibir pequenos sinais de erro apenas
            # quando a tensao ja esta alta. O texto e curto e discreto.
            if self.b_tension >= 60 and flicker_phase == 0:
                monitor_font = pygame.font.SysFont(None, 8)
                monitor_message = (
                    "ERRO B-03"
                    if self.b_tension < 80
                    else "ACESSO NEGADO"
                )
                msg = monitor_font.render(
                    monitor_message,
                    True,
                    (145, 130, 112)
                )
                self.screen.blit(
                    msg,
                    (monitor.x + 5, monitor.y + 16)
                )

            # Suporte e base claramente apoiados sobre a mesa.
            pygame.draw.rect(self.screen, (28, 24, 20), (770, 265, 12, 10))
            pygame.draw.rect(self.screen, (45, 38, 30), (758, 275, 36, 5))

            # Teclado e mouse apoiados na mesma mesa do computador.
            pygame.draw.rect(self.screen, (38, 34, 29), (718, 269, 34, 7))
            pygame.draw.rect(self.screen, (55, 47, 38), (754, 270, 6, 6))

            # Uma cadeira ligeiramente deslocada da mesa, dando mais vida ao ambiente.
            pygame.draw.rect(self.screen, (45, 31, 24), (750, 301, 34, 26))
            pygame.draw.rect(self.screen, (25, 20, 17), (754, 295, 26, 10))
            pygame.draw.rect(self.screen, (35, 27, 21), (762, 327, 7, 16))

            # Pequenos papeis espalhados sobre algumas mesas.
            # Agora eles parecem folhas de verdade, com cabecalho e
            # pequenas linhas de texto escritas.
            paper_font = pygame.font.SysFont(None, 9)

            def draw_paper(rect, heading, lines, clue=0):
                paper = pygame.Rect(rect)
                if isinstance(lines, int):
                    lines = range(lines)
                paper_color = (224, 218, 199)
                paper_edge = (135, 128, 111)
                ink = (58, 54, 47)

                pygame.draw.rect(self.screen, paper_color, paper)
                pygame.draw.rect(self.screen, paper_edge, paper, 1)

                # Cabecalho
                title = paper_font.render(heading, True, ink)
                title_pos = title.get_rect(
                    x=paper.x + 2,
                    y=paper.y + 2
                )
                self.screen.blit(title, title_pos)

                # Pequenas linhas de texto
                line_y = paper.y + 9
                for i, _ in enumerate(lines):
                    end_x = paper.right - 2
                    # Variacao pequena nas linhas para parecer texto digitado/escrito.
                    if clue % 3 == 1 and i == 1:
                        end_x -= 6
                    elif clue % 3 == 2 and i == 0:
                        end_x -= 3
                    pygame.draw.line(
                        self.screen,
                        ink,
                        (paper.x + 2, line_y),
                        (end_x, line_y),
                        1
                    )
                    line_y += 4

                # Detalhes extras: pequenas marcas que fazem cada folha
                # parecer um documento diferente, sem transformar a tela em texto legivel demais.
                if clue == 1:
                    pygame.draw.rect(self.screen, (95, 90, 80), (paper.right - 7, paper.y + 3, 3, 2))
                    pygame.draw.line(self.screen, (95, 90, 80), (paper.x + 3, paper.bottom - 3), (paper.x + 13, paper.bottom - 3), 1)
                elif clue == 2:
                    pygame.draw.line(self.screen, (88, 82, 72), (paper.x + 3, paper.bottom - 4), (paper.right - 4, paper.bottom - 4), 1)
                    pygame.draw.rect(self.screen, (72, 66, 56), (paper.x + 3, paper.bottom - 7, 2, 2))
                elif clue == 3:
                    pygame.draw.rect(self.screen, (88, 82, 72), (paper.right - 8, paper.bottom - 6, 4, 3), 1)
                    pygame.draw.line(self.screen, (88, 82, 72), (paper.x + 3, paper.y + 11), (paper.x + 8, paper.y + 11), 1)

                # A partir de tensao mais alta, uma folha ganha uma marca vermelha sutil.
                if self.b_tension >= 60 and heading == "B-03":
                    pygame.draw.line(self.screen, (120, 45, 40), (paper.right - 8, paper.y + 3), (paper.right - 3, paper.y + 3), 1)

            draw_paper((168, 245, 34, 22), "RELATORIO", 3, 1)
            draw_paper((220, 260, 30, 20), "B-03", 2, 2)
            draw_paper((680, 255, 30, 21), "SETOR B", 3, 3)
            draw_paper((800, 265, 27, 19), "OK", 2, 1)
            draw_paper((323, 480, 32, 21), "AVISO", 3, 2)

            # -------------------------------------------------
            # ILUMINARIAS ESTRANHAS — ESCRITORIO B
            # -------------------------------------------------
            # A ideia aqui e que as luminarias nao pisquem todas juntas.
            # Cada uma falha em um ritmo diferente, criando a sensacao
            # de que a energia da sala esta ficando instavel.
            tension = self.b_tension
            t = pygame.time.get_ticks() / 1000.0

            luminarias = [
                (250, 100, 118, 7, 0.00),
                (500, 100, 118, 7, 0.37),
                (750, 100, 118, 7, 0.74),
                (1000, 100, 118, 7, 1.11),
            ]

            # Em tensao baixa, quase tudo permanece normal.
            # Em tensao alta, algumas luminarias apagam por instantes
            # e fazem pequenos pulsos irregulares.
            light_darkness = 0.0
            for index, (lx, ly, lw, lh, offset) in enumerate(luminarias):
                phase = int((t + offset) * (1.15 + index * 0.07))
                cycle = phase % 11

                light_on = True
                pulse = False

                if tension < 20:
                    light_on = cycle not in (10,)
                elif tension < 40:
                    light_on = cycle not in (5, 10)
                elif tension < 60:
                    light_on = cycle not in (3, 7, 10)
                    pulse = cycle in (2, 6)
                elif tension < 80:
                    light_on = cycle not in (2, 4, 8, 10)
                    pulse = cycle in (1, 5, 9)
                else:
                    light_on = cycle not in (1, 2, 4, 6, 7, 10)
                    pulse = cycle in (3, 5, 8)

                # Estrutura da luminaria
                pygame.draw.rect(
                    self.screen,
                    (28, 25, 22),
                    (lx - 4, ly - 4, lw + 8, 15)
                )
                pygame.draw.rect(
                    self.screen,
                    (54, 49, 42),
                    (lx, ly, lw, lh),
                    1
                )

                if light_on:
                    if pulse:
                        light_color = (178, 170, 137)
                        light_darkness += 0.035
                    else:
                        light_color = (92, 86, 70) if tension < 60 else (77, 71, 58)
                    pygame.draw.rect(self.screen, light_color, (lx + 2, ly + 2, lw - 4, lh - 4))
                else:
                    pygame.draw.rect(self.screen, (30, 28, 25), (lx + 2, ly + 2, lw - 4, lh - 4))
                    light_darkness += 0.055

            # Alguns apagaoes devem alterar levemente a iluminacao geral,
            # sem deixar a sala completamente preta.
            if tension >= 40 and light_darkness > 0.0:
                dark_alpha = min(36, int(110 * light_darkness))
                dark_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                dark_surface.fill((0, 0, 0, dark_alpha))
                self.screen.blit(dark_surface, (0, 0))

            # Em tensao alta, uma luminaria pode dar um pulso bem rapido
            # de claridade antes de voltar ao estado falho.
            if tension >= 60:
                strobe_phase = int(t * 13) % 29
                if strobe_phase in (3, 4):
                    strobe_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    strobe_surface.fill((220, 215, 190, 18))
                    self.screen.blit(strobe_surface, (0, 0))

            # A partir de 60, uma das folhas parece levemente fora
            # do lugar. A mudanca e minima para continuar sutil.
            paper_shift = 0
            if tension >= 60:
                paper_shift = 2 if int(t * 0.8) % 2 == 0 else 0

            # Reforca visual do papel do meio quando a tensao aumenta.
            # O detalhe continua pequeno e nao interfere na coleta.
            if tension >= 60:
                small_paper = pygame.Rect(680 + paper_shift, 188, 30, 21)
                pygame.draw.rect(self.screen, (224, 218, 199), small_paper)
                pygame.draw.rect(self.screen, (135, 128, 111), small_paper, 1)
                pygame.draw.line(self.screen, (58, 54, 47), (small_paper.x + 2, small_paper.y + 12), (small_paper.right - 2, small_paper.y + 12), 1)
                pygame.draw.line(self.screen, (58, 54, 47), (small_paper.x + 2, small_paper.y + 16), (small_paper.right - 5, small_paper.y + 16), 1)

            # Em 80+, o monitor deixa de parecer apenas um computador
            # ligado: surge um brilho intermitente bem discreto.
            if tension >= 80 and flicker_phase == 0:
                pygame.draw.rect(self.screen, (110, 110, 94), monitor.inflate(-11, -11), 1)

            # Um pequeno ponto de luz ao fundo, quase imperceptivel.
            if self.b_tension >= 40 and flicker_phase == 0:
                pygame.draw.rect(self.screen, (170, 170, 140), (770, 280, 3, 14))

        # -------------------------
        # DOCUMENTOS
        # -------------------------

        docs_text = self.font.render(
            f"Documentos: {self.documents_collected}/3",
            True,
            WHITE
        )

        self.screen.blit(
            docs_text,
            (850, 60)
        )

        for doc in self.get_current_documents():
            if not doc.collected:
                doc.draw(self.screen, self.camera)

        # -------------------------
        # ESTAÇÃO
        # -------------------------

        # Mesa/estacao de avaliacao com detalhes de um computador.
        station = self.get_current_station()
        pygame.draw.rect(
            self.screen,
            (40, 40, 40),
            station
        )
        pygame.draw.rect(
            self.screen,
            (24, 24, 24),
            (station.x + 28, station.y + 10, 84, 34),
            border_radius=3
        )
        pygame.draw.rect(
            self.screen,
            (18, 19, 21),
            (station.x + 34, station.y + 15, 72, 23),
            border_radius=2
        )

        # V57: a tela sinaliza quando a estacao esta pronta para a avaliacao.
        if self.current_room == "office_a":
            station_label = (
                "PRONTA"
                if self.documents_collected >= 3 and not self.evaluation_finished
                else "AGUARDE"
            )
            label_font = pygame.font.SysFont("arial", 10, bold=True)
            label_surface = label_font.render(station_label, True, (175, 185, 165))
            self.screen.blit(label_surface, (station.x + 43, station.y + 21))
        pygame.draw.rect(
            self.screen,
            (55, 55, 55),
            (station.x + 64, station.y + 44, 12, 8)
        )
        pygame.draw.rect(
            self.screen,
            (65, 65, 65),
            (station.x + 50, station.y + 54, 40, 7),
            border_radius=2
        )
        pygame.draw.rect(
            self.screen,
            (48, 45, 40),
            (station.x + 36, station.y + 65, 48, 6),
            border_radius=2
        )
        pygame.draw.circle(
            self.screen,
            (150, 150, 145),
            (station.x + 95, station.y + 68),
            3
        )

        station_text = self.font.render(
            "AVALIACAO",
            True,
            WHITE
        )

        self.screen.blit(
            station_text,
            (
                self.get_current_station().x + 10,
                self.get_current_station().y + 25
            )
        )

        # -------------------------
        # SAÍDA
        # -------------------------

        if self.evaluation_finished and not self.b_boss_reveal_pending:

            exit_color = GREEN
            if self.current_office == "B" and self.b_insane_active:
                pulse = 90 + int(60 * (0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 180.0)))
                exit_color = (pulse, 40, 40)

            pygame.draw.rect(
                self.screen,
                exit_color,
                self.get_current_exit()
            )

            exit_text = self.font.render(
                "SAIDA",
                True,
                BLACK
            )

            self.screen.blit(
                exit_text,
                (
                    self.get_current_exit().x + 25,
                    self.get_current_exit().y + 25
                )
            )

        # -------------------------
        # CHEFE
        # -------------------------

        if self.boss_active:
            self.boss.draw(
                self.screen
            )

        # -------------------------
        # JOGADOR
        # -------------------------

        self.player.draw(
            self.screen,
            self.camera
        )

        # -------------------------
        # HUD DO ESCRITORIO
        # -------------------------
        if self.current_office == "B":
            tension_label = self.font.render(
                f"Tensao: {int(self.b_tension)}/100",
                True,
                WHITE
            )
            self.screen.blit(tension_label, (20, 20))

            pygame.draw.rect(self.screen, (80, 80, 80), (20, 55, 220, 18))
            pygame.draw.rect(
                self.screen,
                (200, 30, 30),
                (20, 55, int(220 * (self.b_tension / self.b_tension_max)), 18)
            )

            if self.boss_active:
                state_names = {
                    "patrol": "CHEFE: PATRULHANDO",
                    "heard": "CHEFE: OUVIU PASSOS",
                    "search": "CHEFE: PROCURANDO",
                    "chase": "CHEFE: PERSEGUINDO",
                    "insane": "CHEFE: INSANO"
                }
                state_text = self.font.render(
                    state_names.get(self.boss_state, ""),
                    True,
                    (255, 80, 80)
                )
                self.screen.blit(state_text, (20, 80))

                if self.boss_alert_text and self.boss_alert_timer > 0:
                    alert_text = self.font.render(
                        self.boss_alert_text,
                        True,
                        (255, 220, 80)
                    )
                    self.screen.blit(alert_text, (20, 115))

        elif self.current_office == "A":
            # No A nao existe HUD de raiva/tensao.
            # A unica barra e a de erros da avaliacao.
            if self.evaluation_started:
                pygame.draw.rect(self.screen, (80, 80, 80), (20, 55, 220, 18))
                error_ratio = min(1.0, self.math.wrong_answers / 3.0)
                pygame.draw.rect(
                    self.screen,
                    (200, 30, 30),
                    (20, 55, int(220 * error_ratio), 18)
                )

        # -------------------------
        # STATUS DA AVALIAÇÃO
        # -------------------------

        if self.evaluation_started:

            status = self.font.render(
                f"Acertos: {self.math.correct_answers}   "
                f"Erros: {self.math.wrong_answers}",
                True,
                WHITE
            )

            self.screen.blit(
                status,
                (20, 20)
            )

    # =====================================================
    # CORRUPÇÃO DINÂMICA — ESCRITÓRIO B
    # =====================================================

    def _corrupt_dynamic_text(self, value, level, salt=0):
        if level <= 0:
            return value

        # Corrupção mais lenta: continua viva, mas sem trocar
        # de estado rápido demais.
        tick = int(self.b_corruption_anim_timer * (2 + level)) + salt
        state = tick % 12

        if state in (0, 1, 8, 9) and level <= 2:
            return value

        replacements = {
            "A": "4", "a": "4",
            "E": "3", "e": "3",
            "I": "1", "i": "1",
            "O": "0", "o": "0",
            "S": "5", "s": "5",
            "T": "7", "t": "7",
            "R": "Я", "r": "Я",
            "N": "И", "n": "И",
        }

        strength = {
            1: 0.16,
            2: 0.28,
            3: 0.42,
            4: 0.58,
        }.get(level, 0.20)

        chars = list(str(value))

        for i, ch in enumerate(chars):
            if ch.isspace():
                continue

            code = (i * 19 + tick * 7 + salt * 17) % 100

            if code < int(strength * 100):
                if ch.isalpha() and state in (1, 2, 4, 6):
                    chars[i] = replacements.get(ch, ch)
                elif state in (3, 5) and code % 3 == 0:
                    chars[i] = "█"
                elif state == 6 and code % 4 == 0:
                    chars[i] = "_"

        result = "".join(chars)

        if level >= 2 and state in (2, 4, 5) and result:
            pos = (tick * 3 + salt * 11) % len(result)
            if result[pos] != " ":
                result = result[:pos] + "█" + result[pos + 1:]

        return result

    def _draw_question_glitch(self, intensity):
        if intensity <= 0:
            return

        tick = int(self.b_corruption_anim_timer * 4)
        pulse = tick % 18

        # Glitch bem mais espaçado: aparece por pequenos momentos,
        # sem ficar piscando/trocando a tela o tempo todo.
        if pulse not in (7, 8, 9):
            return

        rng = random.Random(tick + intensity * 97)

        for _ in range(1 + intensity):
            y = rng.randint(190, 610)
            h = rng.randint(1, 3 + intensity)
            shift = rng.randint(
                -12 - intensity * 5,
                12 + intensity * 5
            )

            strip = self.screen.subsurface(
                pygame.Rect(
                    0,
                    y,
                    WIDTH,
                    min(h, HEIGHT - y)
                )
            ).copy()

            self.screen.blit(strip, (shift, y))

            if rng.random() < 0.7:
                pygame.draw.rect(
                    self.screen,
                    (120, 120, 120),
                    (
                        rng.randint(100, WIDTH - 180),
                        y,
                        rng.randint(20, 100),
                        1
                    )
                )

    # =====================================================
    # DESENHAR QUESTÃO
    # =====================================================

    def draw_math_question(self):

        # Fundo escuro leve: mantem o mapa visivel durante a avaliacao.
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 115))
        self.screen.blit(overlay, (0, 0))

        # Painel central discreto para manter textos faceis de ler.
        panel = pygame.Surface((900, 470), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 120))
        self.screen.blit(panel, (WIDTH // 2 - 450, 165))

        question = (
            self.math.get_current_question()
        )

        if question is None:
            return

        # -------------------------
        # TÍTULO
        # -------------------------

        title = self.big_font.render(
            "AVALIACAO CORROMPIDA" if self.current_office == "B" else "AVALIACAO MATEMATICA",
            True,
            WHITE
        )

        self.screen.blit(
            title,
            (WIDTH // 2 - title.get_width() // 2, 80)
        )

        # -------------------------
        # PROGRESSO
        # -------------------------

        current, total = (
            self.math.get_progress()
        )

        progress = self.font.render(
            f"Questao {current + 1}/{total}",
            True,
            WHITE
        )

        self.screen.blit(
            progress,
            (WIDTH // 2 - progress.get_width() // 2, 140)
        )

        # -------------------------
        # QUESTÃO
        # -------------------------

        if self.current_office == "B":
            display_question = self._corrupt_dynamic_text(
                question["question"],
                self.b_corruption_level,
                salt=3
            )

            tick = int(self.b_corruption_anim_timer * 4)

            question_color = (
                (255, 255, 0)
                if tick % 9 not in (4, 5)
                else (255, 220, 80)
            )

            jitter_x = 0
            jitter_y = 0

            if self.b_corruption_level >= 2:
                jitter_x = (tick % 3) - 1
                jitter_y = ((tick * 2) % 3) - 1

            question_text = self.big_font.render(
                display_question,
                True,
                question_color
            )

            self.screen.blit(
                question_text,
                (
                    WIDTH // 2 -
                    question_text.get_width() // 2 +
                    jitter_x,
                    210 + jitter_y
                )
            )

        else:
            question_text = self.big_font.render(
                question["question"],
                True,
                (255, 255, 0)
            )

            self.screen.blit(
                question_text,
                (
                    WIDTH // 2 -
                    question_text.get_width() // 2,
                    210
                )
            )

        # -------------------------
        # ALTERNATIVAS
        # -------------------------

        for i, answer in enumerate(
            question["answers"]
        ):

            number = i + 1
            y = 300 + i * 70

            if self.current_office == "B":
                display_answer = self._corrupt_dynamic_text(
                    str(answer),
                    self.b_corruption_level,
                    salt=20 + i
                )

                answer_text = self.font.render(
                    f"{number} - {display_answer}",
                    True,
                    WHITE
                )

                extra_x = 0
                if self.b_corruption_level >= 3:
                    extra_x = ((tick + i * 2) % 3) - 1

                self.screen.blit(
                    answer_text,
                    (
                        WIDTH // 2 -
                        answer_text.get_width() // 2 +
                        extra_x,
                        y
                    )
                )

            else:
                answer_text = self.font.render(
                    f"{number} - {answer}",
                    True,
                    WHITE
                )

                self.screen.blit(
                    answer_text,
                    (
                        WIDTH // 2 -
                        answer_text.get_width() // 2,
                        y
                    )
                )

        if self.current_office == "B":
            self._draw_question_glitch(
                min(4, self.b_corruption_level)
            )

        # -------------------------
        # INSTRUÇÃO
        # -------------------------

        instruction = self.font.render(
            "Pressione 1, 2, 3 ou 4 para responder",
            True,
            WHITE
        )

        self.screen.blit(
            instruction,
            (
                WIDTH // 2 -
                instruction.get_width() // 2,
                620
            )
        )

    # =====================================================
    # TELA DE VITÓRIA
    # =====================================================

    def draw_victory(self):

        # Encerramento cinematografico da Fase 1 em 4 momentos.
        # O objetivo aqui e criar uma pausa narrativa sem alterar a progressao.
        t = self.phase1_ending_timer

        # Fundo escuro com uma pequena variacao de intensidade.
        pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() / 850.0)
        base_alpha = int(218 + 10 * pulse)

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 4, 5, base_alpha))
        self.screen.blit(overlay, (0, 0))

        # Vinheta discreta para puxar o olhar para o centro.
        for margin, alpha in ((0, 28), (45, 20), (90, 12)):
            pygame.draw.rect(
                self.screen,
                (0, 0, 0, alpha),
                pygame.Rect(margin, margin, WIDTH - margin * 2, HEIGHT - margin * 2),
                width=18
            )

        # -------------------------------------------------
        # MOMENTO 1 — O turno terminou
        # -------------------------------------------------
        if t < 3.2:
            progress = max(0.0, min(1.0, t / 1.2))
            alpha = int(255 * progress)

            title = self.big_font.render(
                "SEU PRIMEIRO TURNO TERMINOU.",
                True,
                (235, 235, 235)
            )
            title.set_alpha(alpha)
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, 245)
            )

            sub = self.font.render(
                "Por alguns segundos, tudo parece normal.",
                True,
                (150, 150, 150)
            )
            sub.set_alpha(alpha)
            self.screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2, 305)
            )

        # -------------------------------------------------
        # MOMENTO 2 — Clara
        # -------------------------------------------------
        elif t < 7.0:
            title = self.big_font.render(
                "CLARA",
                True,
                WHITE
            )
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, 205)
            )

            line = self.font.render(
                "Ela escuta em silencio e olha para a porta do Escritorio B.",
                True,
                (185, 185, 185)
            )
            self.screen.blit(
                line,
                (WIDTH // 2 - line.get_width() // 2, 275)
            )

            # Pequeno indicador visual da porta, sem revelar demais.
            door = pygame.Rect(WIDTH // 2 - 42, 355, 84, 150)
            pygame.draw.rect(self.screen, (24, 24, 26), door)
            pygame.draw.rect(self.screen, (72, 72, 76), door, 2)
            pygame.draw.rect(self.screen, (120, 45, 42), (door.x + 8, door.y + 8, 5, door.height - 16))

            warning = self.font.render(
                "SETOR B",
                True,
                (125, 75, 70)
            )
            self.screen.blit(
                warning,
                (WIDTH // 2 - warning.get_width() // 2, 525)
            )

        # -------------------------------------------------
        # MOMENTO 3 — Algo permaneceu
        # -------------------------------------------------
        elif t < 10.8:
            glitch_tick = int(t * 8)
            if glitch_tick % 9 in (0, 1):
                title_text = "ALGUMA COISA AINDA ESTA ERRADA."
                title_x_offset = ((glitch_tick * 13) % 7) - 3
            else:
                title_text = "ALGUMA COISA AINDA ESTA ERRADA."
                title_x_offset = 0

            title = self.big_font.render(
                title_text,
                True,
                (205, 205, 205)
            )
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2 + title_x_offset, 250)
            )

            sub = self.font.render(
                "Mas o turno acabou.",
                True,
                (120, 120, 120)
            )
            self.screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2, 315)
            )

            # Um risco curto aparece e desaparece, lembrando a corrupcao do B.
            if glitch_tick % 5 == 0:
                pygame.draw.rect(
                    self.screen,
                    (105, 45, 42),
                    (WIDTH // 2 - 145, 375, 290, 2)
                )

        # -------------------------------------------------
        # MOMENTO 4 — Fechamento
        # -------------------------------------------------
        else:
            title = self.big_font.render(
                "FASE 1 CONCLUIDA",
                True,
                GREEN
            )
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, 165)
            )

            result = self.font.render(
                "O turno acabou. Mas alguma coisa continua errada.",
                True,
                WHITE
            )
            self.screen.blit(
                result,
                (WIDTH // 2 - result.get_width() // 2, 245)
            )

            hint = self.font.render(
                "Acertos: {}    Erros: {}".format(
                    self.math.correct_answers,
                    self.math.wrong_answers
                ),
                True,
                (150, 150, 150)
            )
            self.screen.blit(
                hint,
                (WIDTH // 2 - hint.get_width() // 2, 305)
            )

            # Fechamento sem revelar a Fase 2 inteira.
            teaser = self.font.render(
                "A historia ainda nao terminou.",
                True,
                (115, 115, 115)
            )
            self.screen.blit(
                teaser,
                (WIDTH // 2 - teaser.get_width() // 2, 385)
            )

            # Barra final puramente visual.
            bar = pygame.Rect(WIDTH // 2 - 180, 455, 360, 2)
            pygame.draw.rect(self.screen, (65, 65, 68), bar)
            progress = max(0.0, min(1.0, (t - 10.8) / 3.2))
            fill = bar.copy()
            fill.width = int(bar.width * progress)
            if fill.width > 0:
                pygame.draw.rect(self.screen, (135, 135, 140), fill)

    # =====================================================
    # IA DO CHEFE
    # =====================================================

    def update_boss_ai(self, dt):
        """
        IA do chefe:

        VISÃO:
            obstáculos bloqueiam a linha de visão.

        AUDIÇÃO:
            andar faz pouco barulho; correr faz muito barulho.

        MOVIMENTO:
            patrulha livre -> ouviu -> investiga -> viu -> persegue.
        """

        player_pos = pygame.Vector2(self.player.rect.center)
        boss_pos = pygame.Vector2(self.boss.rect.center)
        distance_to_player = boss_pos.distance_to(player_pos)

        if self.boss_alert_timer > 0:
            self.boss_alert_timer -= dt
            if self.boss_alert_timer <= 0:
                self.boss_alert_text = ""

        can_see = self.can_boss_see_player(distance_to_player)
        is_moving, is_running = self.get_player_movement_state()

        heard = False
        if is_moving:
            hearing_radius = (
                self.boss_hearing_run_radius
                if is_running
                else self.boss_hearing_walk_radius
            )
            heard = distance_to_player <= hearing_radius

        # =====================================================
        # PATRULHA LIVRE
        # =====================================================
        if self.boss_state == "patrol":

            if can_see:
                self.boss_state = "chase"
                self.boss_last_seen = player_pos
                self.boss_lost_sight_timer = 0.0
                self.boss_alert_text = "CHEFE: VIU VOCE!"
                self.boss_alert_timer = 1.2
                return

            if heard:
                self.boss_state = "heard"
                self.boss_last_seen = player_pos
                self.boss_search_timer = 0.0
                self.boss_alert_text = "CHEFE: OUVIU PASSOS..."
                self.boss_alert_timer = 1.5
                return

            if self.boss_roam_wait > 0:
                self.boss_roam_wait -= dt
                return

            if self.boss_roam_target is None:
                self.boss_roam_target = self.get_random_boss_patrol_target()

            if self.boss_roam_target is not None:
                self.move_boss_towards(
                    self.boss_roam_target,
                    1.35,
                    dt
                )

                if self.distance_boss_to(self.boss_roam_target) < 25:
                    self.boss_roam_target = None
                    self.boss_roam_wait = random.uniform(0.2, 0.8)

        # =====================================================
        # OUVIU PASSOS
        # =====================================================
        elif self.boss_state == "heard":

            self.boss_search_timer += dt

            if can_see:
                self.boss_state = "chase"
                self.boss_last_seen = player_pos
                self.boss_lost_sight_timer = 0.0
                self.boss_alert_text = "CHEFE: TE ENCONTROU!"
                self.boss_alert_timer = 1.2
                return

            if heard:
                # O som atualiza a região aproximada.
                self.boss_last_seen = player_pos
                self.boss_search_timer = 0.0

            if self.boss_last_seen is not None:
                target = pygame.Vector2(self.boss_last_seen)

                self.move_boss_towards(
                    target,
                    1.55,
                    dt
                )

                if self.distance_boss_to(target) < 30:
                    self.boss_last_seen = None

            if self.boss_search_timer >= self.boss_search_duration:
                self.boss_state = "patrol"
                self.boss_search_timer = 0.0
                self.boss_roam_target = None

        # =====================================================
        # PROCURANDO
        # =====================================================
        elif self.boss_state == "search":

            self.boss_search_timer += dt

            if can_see:
                self.boss_state = "chase"
                self.boss_last_seen = player_pos
                self.boss_lost_sight_timer = 0.0
                return

            if heard:
                self.boss_last_seen = player_pos
                self.boss_search_timer = 0.0

            if self.boss_last_seen is not None:
                target = pygame.Vector2(self.boss_last_seen)

                self.move_boss_towards(
                    target,
                    1.65,
                    dt
                )

                if self.distance_boss_to(target) < 30:
                    self.boss_last_seen = None

            if self.boss_search_timer >= self.boss_search_duration:
                self.boss_state = "patrol"
                self.boss_search_timer = 0.0
                self.boss_lost_sight_timer = 0.0
                self.boss_roam_target = None

        # =====================================================
        # PERSEGUINDO
        # =====================================================
        elif self.boss_state == "chase":

            if can_see:
                self.boss_last_seen = player_pos
                self.boss_lost_sight_timer = 0.0

                self.move_boss_towards(
                    player_pos,
                    2.15,
                    dt
                )

            else:
                self.boss_lost_sight_timer += dt

                if self.boss_last_seen is not None:
                    self.move_boss_towards(
                        pygame.Vector2(self.boss_last_seen),
                        2.0,
                        dt
                    )

                if heard:
                    self.boss_last_seen = player_pos
                    self.boss_lost_sight_timer = 0.0
                    self.boss_alert_text = "CHEFE: OUVIU VOCE!"
                    self.boss_alert_timer = 1.0

                if self.boss_lost_sight_timer >= self.boss_lost_sight_time:
                    self.boss_state = "search"
                    self.boss_search_timer = 0.0
                    self.boss_lost_sight_timer = 0.0

        # =====================================================
        # INSANO
        # =====================================================
        elif self.boss_state == "insane":

            self.boss_last_seen = player_pos

            self.move_boss_towards(
                player_pos,
                4.2,
                dt
            )

    # =====================================================
    # VISÃO
    # =====================================================

    def can_boss_see_player(self, distance):
        if distance > self.boss_vision_radius:
            return False

        start = self.boss.rect.center
        end = self.player.rect.center

        for obstacle in self.office_obstacles:
            if obstacle.clipline(start, end):
                return False

        return True

    # =====================================================
    # AUDIÇÃO / MOVIMENTO
    # =====================================================

    def get_player_movement_state(self):
        keys = pygame.key.get_pressed()

        moving = bool(
            keys[pygame.K_a]
            or keys[pygame.K_d]
            or keys[pygame.K_w]
            or keys[pygame.K_s]
            or keys[pygame.K_LEFT]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_UP]
            or keys[pygame.K_DOWN]
        )

        running = moving and bool(
            keys[pygame.K_LSHIFT]
            or keys[pygame.K_RSHIFT]
        )

        return moving, running

    # =====================================================
    # PONTO ALEATÓRIO DE PATRULHA
    # =====================================================

    def get_random_boss_patrol_target(self):
        room = self.get_boss_room_bounds()

        for _ in range(50):

            x = random.randint(
                room.left + 30,
                room.right - 30
            )

            y = random.randint(
                room.top + 30,
                room.bottom - 30
            )

            candidate = pygame.Rect(
                x - 15,
                y - 15,
                30,
                30
            )

            if any(
                candidate.colliderect(obstacle)
                for obstacle in self.office_obstacles
            ):
                continue

            return pygame.Vector2(x, y)

        return None

    def distance_boss_to(self, target):
        boss_pos = pygame.Vector2(self.boss.rect.center)
        return boss_pos.distance_to(target)

    def boss_rect_at(self, center_x, center_y):
        rect = self.boss.rect.copy()
        rect.center = (int(center_x), int(center_y))
        return rect

    def boss_position_is_free(self, center_x, center_y):
        rect = self.boss_rect_at(center_x, center_y)
        room = self.get_boss_room_bounds()

        # O retangulo inteiro do chefe precisa caber no piso.
        if not room.contains(rect):
            return False

        return not any(
            rect.colliderect(obstacle)
            for obstacle in self.get_navigation_obstacles()
        )

    def get_boss_grid_path(self, target):
        """
        A* simples em uma grade.

        Isso resolve o problema que estava acontecendo:
        o chefe encontrava um móvel, encostava nele e continuava
        tentando andar em linha reta.

        Agora ele procura uma rota livre ao redor dos obstáculos.
        """

        start_pos = pygame.Vector2(self.boss.rect.center)
        target_pos = pygame.Vector2(target)

        cell = 35

        room = self.get_boss_room_bounds()
        min_x, max_x = room.left, room.right
        min_y, max_y = room.top, room.bottom

        def to_cell(pos):
            return (
                round((pos.x - min_x) / cell),
                round((pos.y - min_y) / cell)
            )

        def to_world(node):
            return pygame.Vector2(
                min_x + node[0] * cell,
                min_y + node[1] * cell
            )

        start = to_cell(start_pos)
        goal = to_cell(target_pos)

        max_col = round((max_x - min_x) / cell)
        max_row = round((max_y - min_y) / cell)

        def valid(node):
            x, y = node

            if x < 0 or x > max_col:
                return False
            if y < 0 or y > max_row:
                return False

            world = to_world(node)
            return self.boss_position_is_free(
                world.x,
                world.y
            )

        # Se a célula atual estiver ligeiramente sobre um móvel,
        # permite começar mesmo assim.
        start = (
            max(0, min(max_col, start[0])),
            max(0, min(max_row, start[1]))
        )

        goal = (
            max(0, min(max_col, goal[0])),
            max(0, min(max_row, goal[1]))
        )

        if not valid(goal):
            # Procura a célula livre mais próxima do objetivo.
            candidates = []

            for radius in range(1, 8):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        node = (
                            goal[0] + dx,
                            goal[1] + dy
                        )

                        if valid(node):
                            candidates.append(node)

                if candidates:
                    goal = min(
                        candidates,
                        key=lambda n: abs(n[0] - goal[0]) + abs(n[1] - goal[1])
                    )
                    break

        if not valid(start) or not valid(goal):
            return []

        # A*.
        open_set = {start}
        came_from = {}

        g_score = {start: 0}

        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        f_score = {
            start: heuristic(start, goal)
        }

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        while open_set:
            current = min(
                open_set,
                key=lambda n: f_score.get(n, float("inf"))
            )

            if current == goal:
                path = [current]

                while current in came_from:
                    current = came_from[current]
                    path.append(current)

                path.reverse()

                # Converte as células para coordenadas do mundo.
                return [
                    to_world(node)
                    for node in path[1:]
                ]

            open_set.remove(current)

            for dx, dy in directions:
                neighbor = (
                    current[0] + dx,
                    current[1] + dy
                )

                if not valid(neighbor):
                    continue

                tentative = g_score[current] + 1

                if tentative < g_score.get(
                    neighbor,
                    float("inf")
                ):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative

                    f_score[neighbor] = (
                        tentative
                        + heuristic(neighbor, goal)
                    )

                    open_set.add(neighbor)

        return []

    def move_boss_towards(self, target, speed, dt):
        target = pygame.Vector2(target)
        boss_center = pygame.Vector2(self.boss.rect.center)

        # Recalcula a rota com frequencia e tambem quando o alvo muda bastante.
        self.boss_path_timer -= dt
        target_changed = (
            self.boss_path_target is None
            or pygame.Vector2(self.boss_path_target).distance_to(target) > 45
        )

        if (
            self.boss_path_timer <= 0
            or target_changed
            or not self.boss_path
        ):
            self.boss_path = self.get_boss_grid_path(target)
            self.boss_path_target = target.copy()
            self.boss_path_timer = self.boss_path_recalculate

        distance = speed * dt * 60
        moved = False

        if self.boss_path:
            waypoint = pygame.Vector2(self.boss_path[0])
            direction = waypoint - boss_center

            if direction.length_squared() > 4:
                direction.normalize_ip()

                # Primeiro tenta o movimento completo.
                candidate = boss_center + direction * distance
                if self.boss_position_is_free(candidate.x, candidate.y):
                    self.boss.rect.center = (int(candidate.x), int(candidate.y))
                    moved = True
                else:
                    # Se encostou em um canto, tenta deslizar pela lateral.
                    side = pygame.Vector2(-direction.y, direction.x)
                    for offset in (18, -18, 30, -30):
                        candidate = boss_center + side * offset
                        if self.boss_position_is_free(candidate.x, candidate.y):
                            self.boss.rect.center = (int(candidate.x), int(candidate.y))
                            moved = True
                            self.boss_path = []
                            self.boss_path_target = None
                            break

            if self.boss_path:
                waypoint_distance = pygame.Vector2(self.boss.rect.center).distance_to(waypoint)
                if waypoint_distance < 18:
                    self.boss_path.pop(0)

        # Fallback: mesmo sem A*, o chefe tenta avancar em eixos separados.
        if not moved:
            boss_center = pygame.Vector2(self.boss.rect.center)
            direction = target - boss_center

            if direction.length_squared() > 1:
                direction.normalize_ip()

                # Tenta primeiro o eixo de maior distancia.
                axes = []
                if abs(direction.x) >= abs(direction.y):
                    axes = [pygame.Vector2(direction.x, 0), pygame.Vector2(0, direction.y)]
                else:
                    axes = [pygame.Vector2(0, direction.y), pygame.Vector2(direction.x, 0)]

                for axis in axes:
                    if axis.length_squared() == 0:
                        continue
                    candidate = boss_center + axis * distance
                    if self.boss_position_is_free(candidate.x, candidate.y):
                        self.boss.rect.center = (int(candidate.x), int(candidate.y))
                        moved = True
                        break

        # Recuperacao anti-prensamento: se o chefe nao saiu do lugar por um
        # pequeno periodo, ele abandona a rota e procura uma direcao livre.
        new_position = pygame.Vector2(self.boss.rect.center)
        movement_delta = new_position.distance_to(self.boss_last_position)

        if movement_delta < 0.8:
            self.boss_stuck_timer += dt
        else:
            self.boss_stuck_timer = 0.0

        self.boss_last_position = new_position

        if self.boss_stuck_timer >= 0.45:
            self.boss_stuck_timer = 0.0
            self.boss_path = []
            self.boss_path_target = None

            # Procura uma celula livre ao redor do chefe para destravar.
            escape_directions = [
                pygame.Vector2(1, 0), pygame.Vector2(-1, 0),
                pygame.Vector2(0, 1), pygame.Vector2(0, -1),
                pygame.Vector2(1, 1), pygame.Vector2(-1, 1),
                pygame.Vector2(1, -1), pygame.Vector2(-1, -1),
            ]

            # Prioriza a direcao que mais aproxima o alvo.
            escape_directions.sort(
                key=lambda d: (boss_center + d * 42).distance_to(target)
            )

            for escape in escape_directions:
                escape.normalize_ip()
                for amount in (28, 42, 56):
                    candidate = new_position + escape * amount
                    if self.boss_position_is_free(candidate.x, candidate.y):
                        self.boss.rect.center = (int(candidate.x), int(candidate.y))
                        self.boss_path_timer = 0.0
                        return

    # =====================================================
    # RESET DO CHECKPOINT
    # =====================================================

    def reset_office_checkpoint(self):
        self.current_room="office_a" if self.current_office=="A" else "office_b"
        self.office_obstacles=self.office_a_obstacles if self.current_office=="A" else self.office_b_obstacles
        self.player.rect.topleft=(150,500)
        for doc in self.get_current_documents(): doc.collected=False
        self.documents_collected=0; self.math=MathChallenge(); self.evaluation_started=False
        self.evaluation_has_started=False; self.evaluation_finished=False; self.evaluation_intro_timer=0.0; self.escape_transition_timer=0.0; self.recovery_mode=False
        self.b_corruption_level=0; self.b_question_number=0; self.b_question_answered=False; self.b_evaluation_complete=False; self.b_corruption_anim_timer=0.0; self.b_boss_reveal_pending=False; self.b_boss_reveal_timer=0.0; self.b_insane_active=False; self.b_exit_unlocked=False
        self.b_tension=0.0
        self.anger=0
        self.boss_active=False; self.boss.active=False; self.boss_path=[]; self.boss_path_target=None
        self.boss_path_timer=0.0; self.boss.chasing=False; self.boss.speed=1.35; self.boss_state="idle"
        self.boss_roam_target=None; self.boss_roam_wait=0.0; self.boss_search_timer=0; self.boss_last_seen=None
        self.boss_lost_sight_timer=0.0; self.boss_alert_text=""; self.boss_alert_timer=0.0; self.boss.rect.topleft=(1050,180)
        self.game_over=False; self.checkpoint_active=False; self.checkpoint_timer=0
        self.objective="Encontrar os documentos"; self.dialogue.hide()
        self.mission_ui.show("CHECKPOINT","Encontre os 3 documentos novamente.")

    # =====================================================
    # TELA DE DERROTA
    # =====================================================

    def draw_game_over(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT)
        )

        overlay.set_alpha(230)

        overlay.fill(
            (20, 0, 0)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        title = self.big_font.render(
            "VOCE FOI PEGO",
            True,
            (255, 60, 60)
        )

        self.screen.blit(
            title,
            (
                WIDTH // 2 -
                title.get_width() // 2,
                190
            )
        )

        result = self.font.render(
            "O chefe percebeu seus erros.",
            True,
            WHITE
        )

        self.screen.blit(
            result,
            (
                WIDTH // 2 -
                result.get_width() // 2,
                260
            )
        )

        score = self.font.render(
            f"Erros: {self.math.wrong_answers}",
            True,
            WHITE
        )

        self.screen.blit(
            score,
            (
                WIDTH // 2 -
                score.get_width() // 2,
                310
            )
        )

    def reset_b_tension(self):
        self.b_tension = 0.0
        self.b_tension_stage = 0
    def add_b_tension(self, amount):
        if self.current_office != "B":
            return
        self.b_tension = min(self.b_tension_max, max(0.0, self.b_tension + amount))
        if self.b_tension < 20: self.b_tension_stage = 0
        elif self.b_tension < 40: self.b_tension_stage = 1
        elif self.b_tension < 60: self.b_tension_stage = 2
        elif self.b_tension < 80: self.b_tension_stage = 3
        elif self.b_tension < 100: self.b_tension_stage = 4
        else: self.b_tension_stage = 5
    def get_office_room_bounds(self):
        # Este e exatamente o retangulo do piso desenhado na tela.
        return pygame.Rect(100, 100, 1080, 520)
    def get_boss_room_bounds(self):
        return self.get_office_room_bounds()
    def get_navigation_obstacles(self):
        # Tudo que o chefe deve tratar como solido.
        obstacles = list(self.office_obstacles)

        if self.current_office == "B":
            # A estacao de avaliacao tambem ocupa espaco fisico.
            obstacles.append(self.b_math_station.copy())

            # Depois que a saida abre, ela tambem vira uma area bloqueada.
            # Isso impede o chefe de ficar prensado entre a porta e a parede.
            if self.b_exit_unlocked:
                obstacles.append(self.office_b_exit.copy())

        return obstacles
    def get_boss_safe_position(self):
        return self.get_boss_room_bounds()

