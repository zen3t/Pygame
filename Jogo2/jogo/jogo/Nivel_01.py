import pygame
from pygame.transform import scale

pygame.init()

TELA_LARGURA = 800
TELA_ALTURA = int(TELA_LARGURA * 0.8)
tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
pygame.display.set_caption("JOGO EM PYGAME")

relogio = pygame.time.Clock()
FPS = 60

movimento_esquerda = False
movimento_direita = False

BG = (233, 212, 96, 1)


def desenho_bg():
    tela.fill(BG)


class Soldado(pygame.sprite.Sprite):

    def __init__(self,jogador_tipo, x, y, scale, veloc):
        pygame.sprite.Sprite.__init__(self)
        self.jogador_tipo = jogador_tipo
        self.veloc = veloc
        self.direcao = 1
        self.virar = False
        self.lista_animacao = []
        self.index = 0
        for i in range(5):
            img = pygame.image.load(f"img/{self.jogador_tipo}/jogador_img/{i}.png")

        img = pygame.image.load(f"img/{self.jogador_tipo}/jogador_img/0.png")
        self.image = pygame.transform.scale(
            img, (int(img.get_width() * scale), int(img.get_height() * scale))
        )

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def movimento(self, movimento_esquerda, movimento_direita):

        dx = 0
        dy = 0

        if movimento_esquerda:
            dx = - self.veloc
            self.virar = True
            self.direlcao = - 1
        if movimento_direita:
            dx = self.veloc
            self.virar = False
            self.direcao =  1
        # Atualizando os retangulos da imagem
        self.rect.x += dx
        self.rect.y += dy

    def desenho(self):
        tela.blit(pygame.transform.flip(self.image,self.virar,False), self.rect)


jogador = Soldado("jogador",200, 200, 2, 5)

run = True
while run:
    relogio.tick(FPS)
    desenho_bg()
    jogador.desenho()
    jogador.movimento(movimento_direita, movimento_esquerda)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # bloco para apertar as teclas de movimento
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_d:
                movimento_esquerda = True
            if event.key == pygame.K_a:
                movimento_direita = True
            # Tecla de saida do game

            if event.key == pygame.K_ESCAPE:
                run = False

        # Bloco para apertar as teclas de movimento
        if event.type == pygame.KEYUP:

            if event.key == pygame.K_d:
                movimento_esquerda = False
            if event.key == pygame.K_a:
                movimento_direita = False

    pygame.display.update()
pygame.quit()
