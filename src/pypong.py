import pygame 
from pygame.locals import *
from sys import exit
from config import LARGURA_TELA as LARGURA, ALTURA_TELA as ALTURA, FPS, TITULO_JOGO as TITULO, PRETO, BRANCO, VELOCIDADE_RAQUETE, VELOCIDADE_BOLA
from funcoes import mover_bola, verificar_paredes, verificar_colisao_raquete, mover_raquete
import os
from dados import carregar_ranking, salvar_ranking
AMARELO = (255, 255, 0)
AZUL = (0,0,255)
VERDE = (0,255,0)
CINZA_CLARO = (190, 190, 190)
VERMELHO = (255, 0 ,0)
AZUL_MARINHO = (39, 39, 54)


pygame.init()

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_FONTE = os.path.join(PASTA_ATUAL, "..", "assets", "fontes", "determination.ttf")


fonte = pygame.font.Font(CAMINHO_FONTE, 50)
fonte_pequena = pygame.font.Font(CAMINHO_FONTE, 28)


tela = pygame.display.set_mode((LARGURA,ALTURA))
pygame.display.set_caption(TITULO)
CAMINHO_CENARIO = os.path.join(PASTA_ATUAL, "..", "assets", "imagens", "cenario.png")
CAMINHO_CAPA = os.path.join(PASTA_ATUAL, "..", "assets", "imagens", "capa.png")
capa_img = pygame.image.load(CAMINHO_CAPA).convert()
capa_img = pygame.transform.scale(capa_img, (480, 480))
fundo = pygame.image.load(CAMINHO_CENARIO).convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))


tempo_estado = pygame.time.get_ticks()

mesa = pygame.Rect(208, 256, 352, 200)

raquete_esq = pygame.Rect(mesa.left, mesa.centery - 40, 8, 50)
raquete_dir = pygame.Rect(mesa.right - 10, mesa.centery - 40, 8, 50)
bola = pygame.Rect(mesa.centerx - 8, mesa.centery - 8, 12, 12)
vel_bola_x = VELOCIDADE_BOLA
vel_bola_y = VELOCIDADE_BOLA
relogio = pygame.time.Clock()
opcao_pause = 0

vidas_esq = 5
vidas_dir = 5
pontos_p1 = 0
pontos_p2 = 0
nome_p1 = ""
nome_p2 = ""
digitando = "P1"


def desenhar_texto(texto, cor, x, y, fonte_usada=None):
    if fonte_usada is None:
        fonte_usada = fonte
    superficie = fonte_usada.render(texto, True, cor)
    retangulo = superficie.get_rect(center=(x, y))
    tela.blit(superficie, retangulo)

dificuldades= {
    "FACIL": 3,
    "MEDIO": 4,
    "DIFICIL": 6,
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
            if estado == "INTRO_NOME":
                if event.key == K_RETURN:
                    if digitando == "P1" and nome_p1 != "":
                        digitando = "P2"
                    elif digitando == "P2" and nome_p2 != "":
                        estado = "INTRO_CRIADORES"
                        tempo_estado = pygame.time.get_ticks()
                elif event.key == K_BACKSPACE:
                    if digitando == "P1":
                        nome_p1 = nome_p1[:-1]
                    else:
                        nome_p2 = nome_p2[:-1]
                else:
                    letra = event.unicode
                    if letra.isprintable():
                        if digitando == "P1" and len(nome_p1) < 12:
                            nome_p1 += letra
                        elif digitando == "P2" and len(nome_p2) < 12:
                            nome_p2 += letra
            if estado == "MENU":
                if event.key == K_DOWN:
                    opcao_menu+=1
                    if opcao_menu > 2:
                        opcao_menu =0
                elif event.key == K_UP:
                    opcao_menu -=1
                    if opcao_menu < 0:
                        opcao_menu = 2
                elif event.key == K_RETURN:
                    if opcao_menu == 0:
                        pontos_p1 = 0
                        pontos_p2 = 0
                        vidas_esq = 5
                        vidas_dir = 5
                        bola.x = mesa.centerx - 8
                        bola.y = mesa.centery - 8
                        estado = "DIFICULDADE"
                    elif opcao_menu == 1:
                        estado = "RANKING"
                    elif opcao_menu == 2:
                        pygame.quit()
                        exit()

            elif estado == "DIFICULDADE":
                if event.key == K_ESCAPE:
                    estado = "MENU"
                elif event.key == K_1 or event.key == K_KP1:
                    vel_bola_x = dificuldades["FACIL"]
                    vel_bola_y = dificuldades["FACIL"]

                elif event.key == K_2 or event.key == K_KP2:
                    vel_bola_x = dificuldades["MEDIO"]
                    vel_bola_y = dificuldades["MEDIO"]

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
            
            elif estado == "GAME_OVER":
                if event.key == K_RETURN:
                    vidas_esq = 5
                    vidas_dir = 5
                    bola.x = mesa.centerx - 8
                    bola.y = mesa.centery - 8
                    estado = "MENU"

            elif estado == "RANKING":
                if event.key == K_ESCAPE:
                    estado = "MENU"


    if estado == "INTRO_NOME":
        tela.fill(AZUL_MARINHO)
        if digitando == "P1":
            desenhar_texto("Digite o nome do P1:", BRANCO, LARGURA//2, ALTURA//2 - 60)
            desenhar_texto(nome_p1 + "|", AMARELO, LARGURA//2, ALTURA//2 + 10)
        else:
            desenhar_texto("Digite o nome do P2:", BRANCO, LARGURA//2, ALTURA//2 - 60)
            desenhar_texto(nome_p2 + "|", AMARELO, LARGURA//2, ALTURA//2 + 10)
        desenhar_texto("ENTER para confirmar", BRANCO, LARGURA//2, ALTURA//2 + 100, fonte_pequena)
        

    elif estado == "INTRO_CRIADORES":
        tela.fill(PRETO)
        desenhar_texto("Feito por", BRANCO, LARGURA//2, ALTURA//2 - 100)
        desenhar_texto("Guilherme Valadares", BRANCO, LARGURA//2, ALTURA//2 - 30, fonte_pequena)
        desenhar_texto("Pedro Henrique Fonseca",    BRANCO, LARGURA//2, ALTURA//2 + 10, fonte_pequena)
        desenhar_texto("Daniell Cardoso",    BRANCO, LARGURA//2, ALTURA//2 + 50, fonte_pequena)
        desenhar_texto("Vinicius Eduardo",    BRANCO, LARGURA//2, ALTURA//2 + 90, fonte_pequena)
        if pygame.time.get_ticks() - tempo_estado > 2000:
            estado= "MENU"
            tempo_estado = pygame.time.get_ticks()

    elif estado == "MENU":
        tela.fill(AZUL_MARINHO)
        capa_x = LARGURA - capa_img.get_width()
        capa_y = ALTURA - capa_img.get_height()
        tela.blit(capa_img, (capa_x, capa_y))
        desenhar_texto("PYPONG", BRANCO, LARGURA//2, 90)
        if opcao_menu == 0:
            desenhar_texto("JOGAR", AMARELO, LARGURA//2, 180, fonte_pequena)
        else:
            desenhar_texto("JOGAR", BRANCO, LARGURA//2, 180, fonte_pequena)
        if opcao_menu == 1:
            desenhar_texto("RANKING", AMARELO, LARGURA//2, 240, fonte_pequena)
        else:
            desenhar_texto("RANKING", BRANCO, LARGURA//2, 240, fonte_pequena)
        if opcao_menu == 2:
            desenhar_texto("SAIR", AMARELO, LARGURA//2, 300, fonte_pequena)
        else:
            desenhar_texto("SAIR", BRANCO, LARGURA//2, 300, fonte_pequena)

    elif estado == "DIFICULDADE":
        tela.fill(PRETO)
        desenhar_texto("Escolha a dificuldade", BRANCO, LARGURA//2, 150)
        desenhar_texto("1 - Facil", BRANCO, LARGURA//2, 320)
        desenhar_texto("2 - Medio", BRANCO, LARGURA//2, 380)
        desenhar_texto("3 - Dificil", BRANCO, LARGURA//2, 440)

    elif estado == "JOGANDO":
        bola = mover_bola(bola, vel_bola_x, vel_bola_y)
        vel_bola_x, vel_bola_y = verificar_paredes(bola, vel_bola_x, vel_bola_y, mesa)
        vel_bola_x, bateu = verificar_colisao_raquete(bola, vel_bola_x, raquete_esq, raquete_dir)
        if bateu == "ESQ":
            pontos_p1 += 15
        elif bateu == "DIR":
            pontos_p2 += 15

        if bola.left <= mesa.left:
            vidas_esq -= 1
            bola.x = mesa.centerx - 8
            bola.y = mesa.centery - 8
        if bola.right >= mesa.right:
            vidas_dir -= 1
            bola.x = mesa.centerx - 8
            bola.y = mesa.centery - 8

        teclas = pygame.key.get_pressed()
        if teclas[K_w]:
            mover_raquete(raquete_esq, -1, VELOCIDADE_RAQUETE, mesa)
        if teclas[K_s]:
            mover_raquete(raquete_esq, 1, VELOCIDADE_RAQUETE, mesa)
        if teclas[K_UP]:
            mover_raquete(raquete_dir, -1, VELOCIDADE_RAQUETE, mesa)
        if teclas[K_DOWN]:
            mover_raquete(raquete_dir, 1, VELOCIDADE_RAQUETE, mesa)

        tela.blit(fundo, (0, 0))

        pygame.draw.rect(tela, VERMELHO, raquete_esq)
        pygame.draw.rect(tela, AZUL, raquete_dir)
        pygame.draw.ellipse(tela, CINZA_CLARO, bola)
        desenhar_texto(f"P1: {vidas_esq}", BRANCO, 90, ALTURA - 30, fonte_pequena)
        desenhar_texto(f"P2: {vidas_dir}", BRANCO, LARGURA - 90, ALTURA - 30, fonte_pequena)
        desenhar_texto(str(pontos_p1), BRANCO, 90, ALTURA - 60, fonte_pequena)
        desenhar_texto(str(pontos_p2), BRANCO, LARGURA - 90, ALTURA - 60, fonte_pequena)
        if vidas_esq <= 0 or vidas_dir <= 0:
            if vidas_esq <= 0:
                salvar_ranking(nome_p2, pontos_p2)
            else:
                salvar_ranking(nome_p1, pontos_p1)
            estado = "GAME_OVER"

    elif estado == "PAUSE":
        tela.blit(fundo, (0, 0))
        pygame.draw.rect(tela, VERMELHO, raquete_esq)
        pygame.draw.rect(tela, AZUL, raquete_dir)
        pygame.draw.ellipse(tela, CINZA_CLARO, bola)

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
        tela.fill(PRETO)
        if vidas_esq <= 0:
            desenhar_texto(f"{nome_p2} VENCEU!", AMARELO, LARGURA//2, ALTURA//2 - 50)
        else:
            desenhar_texto(f"{nome_p1} VENCEU!", AMARELO, LARGURA//2, ALTURA//2 - 50)
        desenhar_texto("ENTER para voltar ao menu", BRANCO,LARGURA//2, ALTURA//2 + 30, fonte_pequena)
    elif estado == "RANKING":
        tela.fill(AZUL_MARINHO)
        desenhar_texto("RANKING", BRANCO, LARGURA//2, 70)
        ranking = carregar_ranking()
        if len(ranking) == 0:
            desenhar_texto("Nenhum recorde ainda!", BRANCO, LARGURA//2, ALTURA//2, fonte_pequena)
        else:
            for i, entrada in enumerate(ranking):
                desenhar_texto(f"{i+1}. {entrada['jogador']} - {entrada['pontos']}", BRANCO, LARGURA//2, 150 + i * 60, fonte_pequena)
        desenhar_texto("ESC para voltar", BRANCO, LARGURA//2, ALTURA - 40, fonte_pequena)
    pygame.display.update()
