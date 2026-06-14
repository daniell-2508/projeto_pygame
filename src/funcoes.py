import pygame

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
    if bola.colliderect(raquete_esq) or bola.colliderect(raquete_dir):
        vel_x *= -1
    return vel_x

def mover_raquete(raquete, direcao, velocidade, altura):
    raquete.y += direcao * velocidade
    if raquete.top < 0:
        raquete.top = 0
    if raquete.bottom > altura:
        raquete.bottom = altura