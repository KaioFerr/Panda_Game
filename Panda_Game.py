import pygame
from pygame import Surface
from pygame.locals import *
from sys import exit
import os
from random import randrange
import cx_Freeze

pygame.init()
pygame.mixer.init()


diretorio_principal = os.path.dirname(__file__)
diretorio_imagens = os.path.join(diretorio_principal, 'imagem') #tamanho das imagens: 43x34
diretorio_sons = os.path.join(diretorio_principal, 'sons')

largura = 800
altura = 480

cor_branca = (255,255,255)

tela = pygame.display.set_mode((largura,altura))
pygame.display.set_caption("Panda")


sprite_sheet = pygame.image.load(os.path.join(diretorio_imagens, 'sprite-sheet.png')).convert_alpha()
sprite_sheet_bg = pygame.image.load(os.path.join(diretorio_imagens, 'Slide1.png')).convert_alpha()

som_colisao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'colisao.mp3'))
som_pulo = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pulo.mp3'))
som_pontuacao = pygame.mixer.Sound(os.path.join(diretorio_sons, 'pontuacao.mp3'))

pontos = 0

def exibe_mensagem(msg,tamanho, cor):
    fonte = pygame.font.SysFont('comicssansms', tamanho, True, False)
    msg = f'{msg}'
    texto_formatado = fonte.render(msg, True, cor)
    return texto_formatado


class Background(pygame.sprite.Sprite):
    def __init__(self,pos_x):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet_bg.subsurface((800, 0), (800, 454))
        self.index_lista = 0
        self.rect = self.image.get_rect()
        self.rect.y = 0
        self.rect.x = pos_x*800

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = 0
        self.rect.x -= 9

class Panda(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.imagens_panda = []
        for i in range(4):
            img = sprite_sheet.subsurface((i*43,0), (43,34))
            img = pygame.transform.scale(img, (43*2, 34*2))
            self.imagens_panda.append(img)
        self.aceleracao = 9.81
        self.index_lista = 0
        self.image = self.imagens_panda[self.index_lista]
        self.rect = self.image.get_rect()
        self.radius = 25
        self.pos_y_inicial = altura - 152 - 64 // 2
        self.rect.center = [100, altura - 100]
        self.pulo = False

    def pular(self):
        self.pulo = True

    def update(self):

        if self.pulo:
            if self.rect.y <= 200:
                self.pulo = False
            self.rect.y -= 20 - self.aceleracao
        else:
            if self.rect.y < self.pos_y_inicial:
                self.rect.y += 20  - self.aceleracao
            else:
                self.rect.y = self.pos_y_inicial
        if self.index_lista > 3:
            self.index_lista = 0
        self.index_lista += 0.55
        self.image = self.imagens_panda[int(self.index_lista)]

class Nuvens(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image= sprite_sheet.subsurface((215,0), (43,34))
        self.image = pygame.transform.scale(self.image, (43*1.5, 34*1.5))
        self.rect = self.image.get_rect()
        self.rect.y = randrange(50, 200, 50)
        self.rect.x = largura - randrange(30,300, 90)

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
            self.rect.y = randrange(50, 200, 50)
        self.rect.x -= 9


class Tronco(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite_sheet.subsurface((4 * 43, 0), (43, 34))
        self.image = pygame.transform.scale(self.image, (43 * 2, 34 * 2))
        self.rect = self.image.get_rect()
        self.radius = 40
        self.rect.y = altura - 48*3.89
        self.rect.x = largura

    def update(self):
        if self.rect.topright[0] < 0:
            self.rect.x = largura
        self.rect.x -= 9
        self.rect.y = altura - 48 * 3.89

class Botao:
    def __init__(self, imagem_padrao, imagem_apertada, posicao):
        self.imagem_padrao = pygame.image.load(imagem_padrao)
        self.imagem_apertada = pygame.image.load(imagem_apertada)
        self.imagem_padrao = pygame.transform.scale(self.imagem_padrao, (43*1.5, 34*1.5))
        self.imagem_apertada = pygame.transform.scale(self.imagem_apertada, (43*2, 34*2))
        self.imagem = self.imagem_padrao
        self.rect = self.imagem.get_rect()
        self.posicao = posicao
        self.apertado = False
        self.atualizar()

    def desenhar(self, tela):
        tela.blit(self.imagem, self.rect)

    def apertar(self):
        self.imagem = self.imagem_apertada
        self.apertado = True
        if self.apertado:
            tronco.rect.x = largura
            tronco.rect.y = altura - 48*3
            self.apertado = False

    def soltar(self):
        self.imagem = self.imagem_padrao
        self.apertado = False

    def atualizar(self):
        self.rect = self.imagem.get_rect()
        self.rect.center = self.posicao

class Som_Colidiu(pygame.sprite.Sprite):
    def __init__(self, som):
        self.som = som
    def colidiu(self):
        self.som.play()



todas_as_sprites = pygame.sprite.Group()

for i in range(640*2//43):
    bg = Background(i)
    todas_as_sprites.add(bg)



panda = Panda()
todas_as_sprites.add(panda)

for i in range(4):
    nuvem = Nuvens()
    todas_as_sprites.add(nuvem)


tronco = Tronco()
todas_as_sprites.add(tronco)


grupo_obstaculos = pygame.sprite.Group()
grupo_obstaculos.add(tronco)

botao = Botao("imagem/botao.png", "imagem/botao_apertado.png", (400, 240))

relogio = pygame.time.Clock()
while True:
    relogio.tick(30)
    tela.fill(cor_branca)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if panda.rect.y != panda.pos_y_inicial:
                    pass
                else:
                    som_pulo.play()
                    panda.pular()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if botao.rect.collidepoint(pygame.mouse.get_pos()):
                botao.apertar()

        elif event.type == pygame.MOUSEBUTTONUP:
            colidiu = False
            botao.soltar()

            # Atualiza estado dos objetos
        botao.atualizar()



    colisoes = pygame.sprite.spritecollide(panda, grupo_obstaculos, False, pygame.sprite.collide_circle)

    todas_as_sprites.draw(tela)

    if colisoes:
        pontos = 1
        game_over = exibe_mensagem("Game Over", 40, (255, 250, 250))
        tela.blit(game_over, (325, 180))
        bg = Background(1)
        botao.desenhar(tela)
        pygame.display.update()
        pass

    else:
        pontos += 1
        todas_as_sprites.update()
        resultado = exibe_mensagem(pontos, 40, (0,0,0))
        mensagem_pontos = exibe_mensagem('Pontos: ', 40, (0,0,0))

    if pontos % 100 == 0:
        som_pontuacao.play()

    tela.blit(resultado, (745,30))
    tela.blit(mensagem_pontos, (600,30))

    pygame.display.flip()

