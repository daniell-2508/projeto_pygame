import pygame
from pygame.locals import *
from sys import exit
from config import LARGURA_TELA as LARGURA, ALTURA_TELA as ALTURA, FPS, TITULO_JOGO as TITULO, PRETO, BRANCO, VELOCIDADE_RAQUETE, VELOCIDADE_BOLA
from funcoes import mover_bola, verificar_paredes, verificar_colisao_raquete, mover_raquete

pygame.init()

tela = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption(TITULO)

raquete_esq = pygame.Rect(10, ALTURA//2 - 40, 10, 80)
raquete_dir = pygame.Rect(LARGURA - 20, ALTURA//2 - 40, 10, 80)
bola = pygame.Rect(LARGURA//2 - 8, ALTURA//2 - 8, 16, 16)
vel_bola_x = VELOCIDADE_BOLA
vel_bola_y = VELOCIDADE_BOLA
relogio = pygame.time.Clock()
pausado=False

vidas_esq = 3
vidas_dir = 3

while True:
    relogio.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pausado = not pausado 
    if pausado:
        pygame.display.set_caption("Jogo pausado, pressione ESC para continuar")
        continue

    bola = mover_bola(bola, vel_bola_x, vel_bola_y)
    vel_bola_x, vel_bola_y = verificar_paredes(bola, vel_bola_x, vel_bola_y, LARGURA, ALTURA)
    vel_bola_x = verificar_colisao_raquete(bola, vel_bola_x, raquete_esq, raquete_dir)

    if bola.left <=0:
        vidas_esq-=1
        bola.x = LARGURA//2 -8
        bola.y = ALTURA//2 -8
    if bola.right >=LARGURA:
        vidas_dir-=1
        bola.x = LARGURA//2 -8
        bola.y = ALTURA//2 -8

    teclas = pygame.key.get_pressed()
    if teclas[K_w]:
        mover_raquete(raquete_esq, -1, VELOCIDADE_RAQUETE, ALTURA)
    if teclas[K_s]:
        mover_raquete(raquete_esq, 1, VELOCIDADE_RAQUETE, ALTURA)
    if teclas[K_UP]:
        mover_raquete(raquete_dir, -1, VELOCIDADE_RAQUETE, ALTURA)
    if teclas[K_DOWN]:
        mover_raquete(raquete_dir, 1, VELOCIDADE_RAQUETE, ALTURA)
    tela.fill(PRETO)
    pygame.draw.rect(tela,BRANCO, raquete_esq)
    pygame.draw.rect(tela,BRANCO, raquete_dir)
    pygame.draw.ellipse(tela,BRANCO, bola)
    pygame.display.set_caption(f"P1: {vidas_esq} vidas | P2: {vidas_dir} vidas")
    pygame.display.update()

    cores={
        "branca": (255, 255, 255),
        "preto": (0,0,0),
        "amarelo":(255, 255, 0),
        "azul": (0,0,255),
        "verde": (0,255,0)
        }