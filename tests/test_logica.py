import pygame
from src.funcoes import (
    mover_bola,
    verificar_paredes,
    verificar_colisao_raquete,
    mover_raquete,
)


def test_mover_bola():
    """Deve mover a bola somando a velocidade aos eixos x e y."""
    bola = pygame.Rect(100, 100, 12, 12)
    bola = mover_bola(bola, 5, -3)
    assert bola.x == 105
    assert bola.y == 97


def test_verificar_paredes_bate_no_topo():
    """Deve inverter a velocidade vertical e travar a bola no topo da mesa."""
    mesa = pygame.Rect(0, 0, 400, 300)
    bola = pygame.Rect(190, -2, 12, 12)
    vel_x, vel_y = verificar_paredes(bola, 4, -3, mesa)
    assert vel_y == 3
    assert bola.top == mesa.top


def test_verificar_paredes_bate_no_fundo():
    """Deve inverter a velocidade vertical e travar a bola no fundo da mesa."""
    mesa = pygame.Rect(0, 0, 400, 300)
    bola = pygame.Rect(190, 295, 12, 12)
    vel_x, vel_y = verificar_paredes(bola, 4, 3, mesa)
    assert vel_y == -3
    assert bola.bottom == mesa.bottom


def test_verificar_paredes_sem_colisao():
    """Nao deve alterar a velocidade quando a bola esta longe das paredes."""
    mesa = pygame.Rect(0, 0, 400, 300)
    bola = pygame.Rect(190, 150, 12, 12)
    vel_x, vel_y = verificar_paredes(bola, 4, 3, mesa)
    assert vel_x == 4
    assert vel_y == 3


def test_verificar_colisao_raquete_esquerda():
    """Deve inverter a velocidade horizontal e indicar ESQ ao bater na raquete esquerda vindo da direita."""
    raquete_esq = pygame.Rect(10, 100, 8, 50)
    raquete_dir = pygame.Rect(380, 100, 8, 50)
    bola = pygame.Rect(12, 110, 12, 12)
    vel_x, lado = verificar_colisao_raquete(bola, -5, raquete_esq, raquete_dir)
    assert vel_x == 5
    assert lado == "ESQ"


def test_verificar_colisao_raquete_direita():
    """Deve inverter a velocidade horizontal e indicar DIR ao bater na raquete direita vindo da esquerda."""
    raquete_esq = pygame.Rect(10, 100, 8, 50)
    raquete_dir = pygame.Rect(380, 100, 8, 50)
    bola = pygame.Rect(382, 110, 12, 12)
    vel_x, lado = verificar_colisao_raquete(bola, 5, raquete_esq, raquete_dir)
    assert vel_x == -5
    assert lado == "DIR"


def test_verificar_colisao_raquete_sem_colisao():
    """Nao deve alterar a velocidade quando a bola nao toca em nenhuma raquete."""
    raquete_esq = pygame.Rect(10, 100, 8, 50)
    raquete_dir = pygame.Rect(380, 100, 8, 50)
    bola = pygame.Rect(200, 150, 12, 12)
    vel_x, lado = verificar_colisao_raquete(bola, 5, raquete_esq, raquete_dir)
    assert vel_x == 5
    assert lado is None


def test_mover_raquete_dentro_dos_limites():
    """Deve mover a raquete normalmente quando ela permanece dentro da mesa."""
    mesa = pygame.Rect(0, 0, 400, 300)
    raquete = pygame.Rect(0, 100, 8, 50)
    mover_raquete(raquete, 1, 6, mesa)
    assert raquete.y == 106


def test_mover_raquete_limite_superior():
    """Deve travar a raquete no topo da mesa ao tentar passar do limite superior."""
    mesa = pygame.Rect(0, 0, 400, 300)
    raquete = pygame.Rect(0, 2, 8, 50)
    mover_raquete(raquete, -1, 6, mesa)
    assert raquete.top == mesa.top


def test_mover_raquete_limite_inferior():
    """Deve travar a raquete no fundo da mesa ao tentar passar do limite inferior."""
    mesa = pygame.Rect(0, 0, 400, 300)
    raquete = pygame.Rect(0, 248, 8, 50)
    mover_raquete(raquete, 1, 6, mesa)
    assert raquete.bottom == mesa.bottom