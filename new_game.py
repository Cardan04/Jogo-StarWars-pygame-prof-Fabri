import pygame
import math
import sys
from pygame.locals import *
from utils import Player, Enemy, Cloud, SCREEN_WIDTH, SCREEN_HEIGTH

pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
clock = pygame.time.Clock()

fonte = pygame.font.Font(None, 48)


# === Tela inicial ===
def menu_principal():
    pygame.mixer.music.load("Star_Wars_menu.mp3")
    pygame.mixer.music.play(-1)

    imagem_menu = pygame.image.load("menu.jpg")
    imagem_menu = pygame.transform.scale(imagem_menu, (SCREEN_WIDTH, SCREEN_HEIGTH))

    rodando = True
    while rodando:
        tela.blit(imagem_menu, (0, 0))
        titulo = fonte.render("", True, (255, 255, 0))
        tela.blit(titulo, (SCREEN_WIDTH // 2 - 100, 80))

        texto1 = fonte.render("", True, (255, 255, 255))
        tela.blit(texto1, (100, 250))

        texto2 = fonte.render("", True, (255, 255, 255))
        tela.blit(texto2, (100, 320))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                if evento.key == K_RETURN:   # Start Game
                    rodando = False
                    return "start"
                elif evento.key == K_h:      # História
                    tela_historia()

        pygame.display.flip()
        clock.tick(30)


# === Tela História ===
def tela_historia():
    imagem_historia = pygame.image.load("historia.jpg")
    imagem_historia = pygame.transform.scale(imagem_historia, (SCREEN_WIDTH, SCREEN_HEIGTH))
    rodando = True
    while rodando:
        tela.blit(imagem_historia, (0, 0))
        texto = fonte.render("Pressione ESC para voltar", True, (255, 255, 255))
        tela.blit(texto, (50, 500))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                rodando = False
        pygame.display.flip()
        clock.tick(30)


# === Tela escolha da nave ===
def tela_escolher_nave():
    pygame.mixer.music.stop()
    imagem_escolha = pygame.image.load("escolha_nave.jpg")
    imagem_escolha = pygame.transform.scale(imagem_escolha, (SCREEN_WIDTH, SCREEN_HEIGTH))

    naves = {
        "1": "jet1.png",
        "2": "jet2.png",
        "3": "jet3.png"
    }

    rodando = True
    while rodando:
        tela.blit(imagem_escolha, (0, 0))

        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                if evento.unicode in naves:  # Se apertar 1,2,3
                    return naves[evento.unicode]

        pygame.display.flip()
        clock.tick(30)


# === Tela Game Over ===
def tela_game_over():
    pygame.mixer.music.stop()
    imagem_go = pygame.image.load("game_over.jpg")
    imagem_go = pygame.transform.scale(imagem_go, (SCREEN_WIDTH, SCREEN_HEIGTH))
    rodando = True
    while rodando:
        tela.blit(imagem_go, (0, 0))
        #texto = fonte.render("Pressione V para voltar ao Menu", True, (255, 0, 0))
        #tela.blit(texto, (100, 500))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN and evento.key == K_v:
                rodando = False
        pygame.display.flip()
        clock.tick(30)


# === Tela Vitória ===
def tela_congratulations():
    pygame.mixer.music.stop()
    imagem_vitoria = pygame.image.load("congratulations.jpg")
    imagem_vitoria = pygame.transform.scale(imagem_vitoria, (SCREEN_WIDTH, SCREEN_HEIGTH))
    pygame.mixer.music.load("Star_Wars_final_f.mp3")
    pygame.mixer.music.play(-1)
    rodando = True
    while rodando:
        tela.blit(imagem_vitoria, (0, 0))
        texto = fonte.render("Pressione ESC para sair", True, (255, 255, 255))
        tela.blit(texto, (200, 500))
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN and evento.key == K_ESCAPE:
                rodando = False
        pygame.display.flip()
        clock.tick(30)


# === Gameplay ===
def main_game(img_nave):
    pygame.mixer.music.load("Star_Wars_vilao_f.mp3")
    pygame.mixer.music.play(-1)

    som_sobe = pygame.mixer.Sound("Rising_putter.ogg")
    som_desce = pygame.mixer.Sound("Falling_putter.ogg")
    som_colisao = pygame.mixer.Sound("Collision.ogg")

    jogador = Player(som_sobe, som_desce)
    jogador.surf = pygame.image.load(img_nave).convert()
    jogador.surf.set_colorkey((255, 255, 255))

    inimigos = pygame.sprite.Group()
    nuvens = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(jogador)

    ADDENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(ADDENEMY, 250)
    ADDCLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADDCLOUD, 1000)

    tempo_vitoria = 30_000  # 30 segundos
    tempo_inicio = pygame.time.get_ticks()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == ADDENEMY:
                novoinimigo = Enemy()
                inimigos.add(novoinimigo)
                all_sprites.add(novoinimigo)
            elif evento.type == ADDCLOUD:
                novanuvem = Cloud()
                nuvens.add(novanuvem)
                all_sprites.add(novanuvem)

        pressed_keys = pygame.key.get_pressed()
        jogador.update(pressed_keys)
        inimigos.update()
        nuvens.update()

        tela.fill((135, 206, 250))
        for item in all_sprites:
            tela.blit(item.surf, item.rect)

        # Timer
        tempo_passado = pygame.time.get_ticks() - tempo_inicio
        tempo_restante = max(0, tempo_vitoria - tempo_passado)
        segundos = math.ceil(tempo_restante / 1000)
        texto_tempo = fonte.render(f"Tempo: {segundos:02d}", True, (0, 0, 0))
        tela.blit(texto_tempo, (10, 10))

        # Colisão
        if pygame.sprite.spritecollideany(jogador, inimigos):
            som_colisao.play()
            tela_game_over()
            return

        # Vitória
        if tempo_passado >= tempo_vitoria:
            tela_congratulations()
            return

        pygame.display.flip()
        clock.tick(30)


# === Loop Principal do Programa ===
while True:
    escolha = menu_principal()
    if escolha == "start":
        nave = tela_escolher_nave()
        main_game(nave)
