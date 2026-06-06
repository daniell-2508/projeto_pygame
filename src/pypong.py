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

while True:
    relogio.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    bola = mover_bola(bola, vel_bola_x, vel_bola_y)
    vel_bola_x, vel_bola_y = verificar_paredes(bola, vel_bola_x, vel_bola_y, LARGURA, ALTURA)
    vel_bola_x = verificar_colisao_raquete(bola, vel_bola_x, raquete_esq, raquete_dir)

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
    pygame.display.update()