import pygame 
from pygame.locals import *
from sys import exit
from config import LARGURA_TELA as LARGURA, ALTURA_TELA as ALTURA, FPS, TITULO_JOGO as TITULO, PRETO, BRANCO, VELOCIDADE_RAQUETE, VELOCIDADE_BOLA
from funcoes import mover_bola, verificar_paredes, verificar_colisao_raquete, mover_raquete
import os
AMARELO = (255, 255, 0)
AZUL = (0,0,255)
VERDE = (0,255,0)


pygame.init()

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(PASTA_ATUAL, "..", "assets", "fontes", "DeterminationSansWebRegular-369X.ttf")

fonte = pygame.font.Font(CAMINHO_FONTE, 50)
fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 28)


tela = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption(TITULO)
tempo_estado = pygame.time.get_ticks()

raquete_esq = pygame.Rect(10, ALTURA//2 - 40, 10, 80)
raquete_dir = pygame.Rect(LARGURA - 20, ALTURA//2 - 40, 10, 80)
bola = pygame.Rect(LARGURA//2 - 8, ALTURA//2 - 8, 16, 16)
vel_bola_x = VELOCIDADE_BOLA
vel_bola_y = VELOCIDADE_BOLA
relogio = pygame.time.Clock()
opcao_pause = 0

vidas_esq = 3
vidas_dir = 3



def desenhar_texto(texto, cor, x, y, fonte_usada=None):
    if fonte_usada is None:
        fonte_usada = fonte
    superficie = fonte_usada.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    tela.blit(superficie, retangulo)

dificuldades= {
    "FACIL": 4,
    "MEDIO": 6,
    "DIFICIL": 9,
    }

estado = "INTRO_NOME"
opcao_menu= 0

while True:
    relogio.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if estado == "MENU":
                if event.key == K_DOWN:
                    opcao_menu+=1
                    if opcao_menu > 1:
                        opcao_menu =0
                elif event.key == K_UP:
                    opcao_menu -=1
                    if opcao_menu < 0:
                        opcao_menu =1
                elif event.key == K_RETURN:
                    if opcao_menu == 0:
                        estado = "DIFICULDADE"
                    elif opcao_menu == 1:
                        pygame.quit()
                        exit()

            elif estado == "DIFICULDADE":
                if event.key == K_ESCAPE:
                    estado = "MENU"
                elif event.key == K_1 or event.key == K_KP1:
                    vel_bola_x = dificuldades["FACIL"]
                    vel_bola_y = dificuldades["FACIL"]
                    estado = "JOGANDO"
                elif event.key == K_2 or event.key == K_KP2:
                    vel_bola_x = dificuldades["MEDIO"]
                    vel_bola_y = dificuldades["MEDIO"]
                    estado = "JOGANDO"
                elif event.key == K_3 or event.key == K_KP3:
                    vel_bola_x = dificuldades["DIFICIL"]
                    vel_bola_y = dificuldades["DIFICIL"]
                    estado = "JOGANDO"
                
            elif estado == "JOGANDO":
                if event.key == K_ESCAPE:
                    estado = "PAUSE"
                    opcao_pause = 0

            elif estado == "PAUSE":
                if event.key == K_ESCAPE:
                    estado = "JOGANDO"
                elif event.key == K_DOWN:
                    opcao_pause +=1
                    if opcao_pause >1:
                        opcao_pause =0
                elif event.key == K_UP:
                    opcao_pause -=1
                    if opcao_pause < 0:
                        opcao_pause =1
                elif event.key == K_RETURN:
                    if opcao_pause == 0:
                        estado= "JOGANDO"
                    elif opcao_pause == 1:
                        estado = "MENU"

    if estado == "INTRO_NOME":
        tela.fill(PRETO)
        desenhar_texto("PYPONG", BRANCO, LARGURA//2, ALTURA//2)
        if pygame.time.get_ticks() - tempo_estado > 2000:
            estado= "INTRO_CRIADORES"
            tempo_estado = pygame.time.get_ticks()

    elif estado == "INTRO_CRIADORES":
        tela.fill(PRETO)
        desenhar_texto("Feito por", BRANCO, LARGURA//2, ALTURA//2 - 100)
        desenhar_texto("Guilherme Valadares", BRANCO, LARGURA//2, ALTURA//2 - 30, fonte_pequena)
        desenhar_texto("Pedro Henrique Fonseca",    BRANCO, LARGURA//2, ALTURA//2 + 10, fonte_pequena)
        desenhar_texto("Daniel",    BRANCO, LARGURA//2, ALTURA//2 + 50, fonte_pequena)
        desenhar_texto("Vinicius",    BRANCO, LARGURA//2, ALTURA//2 + 90, fonte_pequena)
        if pygame.time.get_ticks() - tempo_estado > 2000:
            estado= "MENU"
            tempo_estado = pygame.time.get_ticks()

    elif estado == "MENU":
        tela.fill(PRETO)
        desenhar_texto("PYPONG", BRANCO, LARGURA//2, 150)
        if opcao_menu == 0:
            desenhar_texto("JOGAR",AMARELO, LARGURA//2, 350)
        else:
            desenhar_texto("JOGAR", BRANCO, LARGURA//2, 350)
        if opcao_menu == 1:
            desenhar_texto("SAIR", AMARELO, LARGURA//2, 420)
        else:
            desenhar_texto("SAIR", BRANCO, LARGURA//2, 420)

    elif estado == "DIFICULDADE":
        tela.fill(PRETO)
        desenhar_texto("Escolha a dificuldade", BRANCO, LARGURA//2, 150)
        desenhar_texto("1 - Facil", BRANCO, LARGURA//2, 320)
        desenhar_texto("2 - Medio", BRANCO, LARGURA//2, 380)
        desenhar_texto("3 - Dificil", BRANCO, LARGURA//2, 440)

    elif estado == "JOGANDO":
        bola = mover_bola(bola, vel_bola_x, vel_bola_y)
        vel_bola_x, vel_bola_y = verificar_paredes(bola, vel_bola_x, vel_bola_y, LARGURA, ALTURA)
        vel_bola_x = verificar_colisao_raquete(bola, vel_bola_x, raquete_esq, raquete_dir)

        if bola.left <= 0:
            vidas_esq -= 1
            bola.x = LARGURA//2 - 8
            bola.y = ALTURA//2 - 8
        if bola.right >= LARGURA:
            vidas_dir -= 1
            bola.x = LARGURA//2 - 8
            bola.y = ALTURA//2 - 8

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
        pygame.draw.rect(tela, BRANCO, raquete_esq)
        pygame.draw.rect(tela, BRANCO, raquete_dir)
        pygame.draw.ellipse(tela, BRANCO, bola)
        pygame.display.set_caption(f"P1: {vidas_esq} vidas | P2: {vidas_dir} vidas")

    elif estado == "PAUSE":
        tela.fill(PRETO)
        pygame.draw.rect(tela, BRANCO, raquete_esq)
        pygame.draw.rect(tela, BRANCO, raquete_dir)
        pygame.draw.ellipse(tela, BRANCO, bola)

        escurecer = pygame.Surface((LARGURA, ALTURA))
        escurecer.set_alpha(150)
        escurecer.fill(PRETO)
        tela.blit(escurecer, (0, 0))

        pygame.draw.rect(tela, PRETO, (LARGURA//2 - 200, ALTURA//2 - 150, 400, 300))
        pygame.draw.rect(tela, BRANCO, (LARGURA//2 - 200, ALTURA//2 - 150, 400, 300), 4)

        desenhar_texto("PAUSA", BRANCO, LARGURA//2, ALTURA//2 - 90)
        if opcao_pause == 0:
            desenhar_texto("Continuar", AMARELO, LARGURA//2, ALTURA//2 - 10, fonte_pequena)
        else:
            desenhar_texto("Continuar", BRANCO, LARGURA//2, ALTURA//2 - 10, fonte_pequena)
        if opcao_pause == 1:
            desenhar_texto("Voltar ao Menu", AMARELO, LARGURA//2, ALTURA//2 + 60, fonte_pequena)
        else:
            desenhar_texto("Voltar ao Menu", BRANCO, LARGURA//2, ALTURA//2 + 60, fonte_pequena)

    elif estado == "GAME_OVER":
        pass
    pygame.display.update()
