import pygame
import os
from config import LARGURA_TELA as LARGURA, ALTURA_TELA as ALTURA

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(PASTA_ATUAL, "..", "assets", "fontes", "determination.ttf")

fonte = pygame.font.Font(CAMINHO_FONTE, 50)
fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 28)


def mover_bola(bola, vel_x, vel_y):
    bola.x += vel_x
    bola.y += vel_y
    return bola

def verificar_paredes(bola, vel_x, vel_y, mesa):
    if bola.top <= mesa.top:
        bola.top = mesa.top
        vel_y *= -1
    if bola.bottom >= mesa.bottom:
        bola.bottom = mesa.bottom
        vel_y *= -1
    return vel_x, vel_y

def verificar_colisao_raquete(bola, vel_x, raquete_esq, raquete_dir):
    if bola.colliderect(raquete_esq) and vel_x < 0:
        return vel_x * -1, "ESQ"
    if bola.colliderect(raquete_dir) and vel_x > 0:
        return vel_x * -1, "DIR"
    return vel_x, None

def mover_raquete(raquete, direcao, velocidade, mesa):
    raquete.y += direcao * velocidade
    if raquete.top < mesa.top:
        raquete.top = mesa.top
    if raquete.bottom > mesa.bottom:
        raquete.bottom = mesa.bottom

def desenhar_texto(texto, cor, x, y, fonte_usada=None):
    if fonte_usada is None:
        fonte_usada = fonte
    superficie = fonte_usada.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    tela = pygame.display.get_surface() 
    tela.blit(superficie, retangulo)