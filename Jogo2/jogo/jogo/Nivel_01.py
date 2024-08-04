import pygame
import os

pygame.init()


TELA_LARGURA = 800
TELA_ALTURA = int(TELA_LARGURA * 0.8)

tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("JOGO EM PYGAME :")


relogio = pygame.time.Clock()
FPS = 60

GRAVIDADE = 0.75

movimento_esquerda = False
movimento_direita = False
atirar = False

bala_img = pygame.image.load("img/icons/bala.png").convert_alpha()

BG = (233, 212, 96)
GREEN = (60, 179, 113)
BLUE = (0, 0, 255)


def desenho_bg():
    tela.fill(BG)
    pygame.draw.line(tela, GREEN, (0, 300), (TELA_LARGURA, 300))
    pygame.draw.line(tela, BLUE, (0, 635), (TELA_LARGURA, 635))


class Soldado(pygame.sprite.Sprite):
    def __init__(self, jogador_tipo, x, y, scale, velocidade, municao):

        pygame.sprite.Sprite.__init__(self)
        self.vivo = True
        self.jogador_tipo = jogador_tipo
        self.velocidade = velocidade
        self.municao = municao
        self.inicio_municao = municao
        self.vel_y = 0
        self.atirar_bala_count = 0
        self.direcao = 1
        self.pular = False
        self.no_ar = True
        self.virar = False
        self.animacao_lista = []
        self.frame_index = 0
        self.acao = 0
        self.atualizar_tempo = pygame.time.get_ticks()

        animacao_tipo = ["jogador_img", "Correr", "pular"]

        for animacao in animacao_tipo:
            temp_list = []
            numero_de_frames = len(os.listdir(f"img/{self.jogador_tipo}/{animacao}"))
            for i in range(numero_de_frames):
                img = pygame.image.load(
                    f"img/{self.jogador_tipo}/{animacao}/{i}.png"
                ).convert_alpha()
                img = pygame.transform.scale(
                    img, (int(img.get_width() * scale), int(img.get_height() * scale))
                )
                temp_list.append(img)
            self.animacao_lista.append(temp_list)

        self.image = self.animacao_lista[self.acao][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def atualizar(self):
        self.atualizar_animacao()
        if self.atirar_bala_count > 0:
            self.atirar_bala_count -= 1

    def movimento(self, movimento_esquerda, movimento_direita):

        dx = 0
        dy = 0

        if movimento_esquerda:
            dx = -self.velocidade
            self.virar = True
            self.direcao = -1
        if movimento_direita:

            dx = self.velocidade
            self.virar = False
            self.direcao = 1

        if self.pular == True and self.no_ar == False:

            self.vel_y = -11
            self.pular = False
            self.no_ar = True

        self.vel_y += GRAVIDADE
        if self.vel_y > 10:

            self.vel_y
        dy += self.vel_y

        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.no_ar = False

        self.rect.x += dx
        self.rect.y += dy

    def atirar(self):
        if self.atirar_bala_count == 0 and self.municao > 0:
            self.atirar_bala_count = 20
            bala = Bala(
                self.rect.centerx + (0.6 * self.rect.size[0] * self.direcao),
                self.rect.centery,
                self.direcao,
            )
            bala_grupo.add(bala)
            self.municao -= 1

    def atualizar_animacao(self):
        ANIMACAO_FRESH = 100

        self.image = self.animacao_lista[self.acao][self.frame_index]

        if pygame.time.get_ticks() - self.atualizar_tempo > ANIMACAO_FRESH:
            self.atualizar_tempo = pygame.time.get_ticks()
            self.frame_index += 1

        if self.frame_index >= len(self.animacao_lista[self.acao]):
            self.frame_index = 0

    def atualizar_acao(self, new_action):
        if new_action != self.acao:
            self.acao = new_action

            self.frame_index = 0
            self.atualizar_tempo = pygame.time.get_ticks()

    def desenho(self, tela):
        tela.blit(pygame.transform.flip(self.image, self.virar, False), self.rect)


class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):

        pygame.sprite.Sprite.__init__(self)
        self.velocidade = 10
        self.image = bala_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direcao = direcao

    def update(self):

        self.rect.x += self.velocidade * self.direcao

        if self.rect.right < 0 or self.rect.left > TELA_LARGURA:

            self.kill()


bala_grupo = pygame.sprite.Group()


jogador = Soldado("jogador", 200, 200, 2, 5, 20)
inimigo = Soldado("inimigo", 400, 200, 2, 5, 20)


run = True
while run:
    relogio.tick(FPS)

    desenho_bg()

    jogador.atualizar()
    jogador.desenho(tela)
    inimigo.desenho(tela)
    bala_grupo.update()
    bala_grupo.draw(tela)
    if jogador.vivo:
        if atirar:
            jogador.atirar()
        if jogador.no_ar:
            jogador.atualizar_acao(2)

        elif movimento_esquerda or movimento_direita:
            jogador.atualizar_acao(1)
        else:
            jogador.atualizar_acao(0)
        jogador.movimento(movimento_esquerda, movimento_direita)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movimento_esquerda = True
            if event.key == pygame.K_d:
                movimento_direita = True

            if event.key == pygame.K_SPACE:
                atirar = True

            if event.key == pygame.K_w and jogador.vivo:
                jogador.pular = True
            if event.key == pygame.K_ESCAPE:
                run = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                movimento_esquerda = False
            if event.key == pygame.K_d:
                movimento_direita = False
            if event.key == pygame.K_SPACE:
                atirar = False

    pygame.display.update()

pygame.quit()
