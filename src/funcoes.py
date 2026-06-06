import pygame

def mover_bola(bola, vel_x, vel_y):
    bola.x += vel_x
    bola.y += vel_y
    return bola

def verificar_paredes(bola, vel_x, vel_y, largura, altura):
    if bola.top <= 0 or bola.bottom >= altura:
        vel_y *= -1
    if bola.left <= 0 or bola.right >= largura:
        vel_x *= -1
    return vel_x, vel_y

def verificar_colisao_raquete(bola, vel_x, raquete_esq, raquete_dir):
    if bola.colliderect(raquete_esq) or bola.colliderect(raquete_dir):
        vel_x *= -1
    return vel_x

def mover_raquete(raquete, direcao, velocidade, altura):
    raquete.y += direcao * velocidade
    if raquete.top < 0:
        raquete.top = 0
    if raquete.bottom > altura:
        raquete.bottom = altura