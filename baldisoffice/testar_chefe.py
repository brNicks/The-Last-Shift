"""Visualizador independente de sprites do chefe — não altera o progresso do jogo."""
from pathlib import Path
import pygame

ROOT=Path(__file__).resolve().parent
ASSETS=ROOT/'assets'/'sprites'/'v62_neutro'/'chefe'
STAGES=['calmo','irritado','estranho','voz_alterada','insano']
DIRECTIONS=['baixo','cima','esquerda','direita']
STAGE_LABELS=['1 CALMO','2 IRRITADO','3 ESTRANHO','4 ALTERADO','5 INSANO']


def main():
    pygame.init()
    try:
        screen=pygame.display.set_mode((960,560))
        pygame.display.set_caption('The Last Shift - Teste do chefe (V62 Parte 17 — progressao dos estagios)')
        clock=pygame.time.Clock()
        font=pygame.font.SysFont(None,30)
        small=pygame.font.SysFont(None,22)
        frames={}
        for stage in STAGES:
            frames[stage]={}
            for facing in DIRECTIONS:
                frames[stage][facing]=[
                    pygame.image.load(str(ASSETS/stage/facing/f'{n}.png')).convert_alpha()
                    for n in range(4)
                ]
        stage_index=0
        direction='baixo'
        x,y=330.0,345.0
        walk_in_place = False
        running=True
        while running:
            dt=min(clock.tick(60)/1000.0,0.05)
            for event in pygame.event.get():
                if event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE):
                    running=False
                elif event.type==pygame.KEYDOWN and pygame.K_1<=event.key<=pygame.K_5:
                    stage_index=event.key-pygame.K_1
                elif event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
                    walk_in_place = not walk_in_place
            keys=pygame.key.get_pressed()
            dx=dy=0
            if keys[pygame.K_LEFT]: dx=-1
            elif keys[pygame.K_RIGHT]: dx=1
            if keys[pygame.K_UP]: dy=-1
            elif keys[pygame.K_DOWN]: dy=1
            if dx!=0 or dy!=0:
                if abs(dx)>=abs(dy) and dx!=0: direction='esquerda' if dx<0 else 'direita'
                else: direction='cima' if dy<0 else 'baixo'
                x=max(90,min(565,x+dx*130*dt))
                y=max(210,min(468,y+dy*130*dt))
                idx=(pygame.time.get_ticks()//145)%4
            elif walk_in_place:
                idx=(pygame.time.get_ticks()//165)%4
            else:
                idx=1
            sprite=frames[STAGES[stage_index]][direction][idx]
            screen.fill((21,21,25))
            pygame.draw.rect(screen,(56,48,46),(30,125,605,395),border_radius=8)
            pygame.draw.rect(screen,(79,60,47),(80,143,290,58),border_radius=6)
            pygame.draw.rect(screen,(36,29,27),(80,143,290,58),3,border_radius=6)
            pygame.draw.rect(screen,(42,37,39),(690,125,225,390),border_radius=10)
            screen.blit(sprite, (int(x)-sprite.get_width()//2,int(y)-sprite.get_height()+8))
            preview=pygame.transform.scale(sprite,(148,232))
            screen.blit(preview,(725,170))
            title=font.render('THE LAST SHIFT  |  TESTE DO CHEFE', True,(230,220,210))
            screen.blit(title,(30,23))
            instruction=small.render('Setas: andar   |   1 a 5: evolucao   |   ESPACO: andar no lugar   |   ESC: sair',True,(214,198,177))
            screen.blit(instruction,(30,70))
            info=small.render('Visual do chefe: '+STAGE_LABELS[stage_index],True,(237,222,206))
            screen.blit(info,(685,430))
            dlabel={'baixo':'Frente','cima':'Costas','esquerda':'Esquerda','direita':'Direita'}[direction]
            screen.blit(small.render('Direcao: '+dlabel,True,(192,184,170)),(685,465))
            pygame.display.flip()
    finally:
        pygame.quit()


if __name__=='__main__':
    main()
