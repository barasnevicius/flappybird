import pygame, random
from pygame.locals import *
from pygame.sprite import spritecollide

def main():
    class Passaro(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            # IMAGENS DO PASSARO DESCONSIDERANDO ESPAÇOS EM BRANCO DA IMAGEM PNG
            self.imagens = [pygame.image.load('assets/yellowbird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/yellowbird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()]

            self.velocidade = VELOCIDADE_PASSARO
            self.imagem_atual = 0
            self.imagem = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
            self.mask = pygame.mask.from_surface(self.imagem)
            self.rect = self.imagem.get_rect()

            # MEIO DA TELA
            self.rect[0] = LARGURA_TELA / 2
            self.rect[1] = ALTURA_TELA / 2

        def update(self):
            self.imagem_atual = (self.imagem_atual + 1) % 3
            self.image = self.imagens[self.imagem_atual]

            self.velocidade += GRAVIDADE_PASSARO

            self.rect[1] += self.velocidade

        def voar(self):
            self.velocidade = -VELOCIDADE_PASSARO

    class Piso(pygame.sprite.Sprite):
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('assets/base.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (LARGURA_PISO , ALTURA_PISO))
            self.mask = pygame.mask.from_surface(self.image)

            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = ALTURA_TELA - ALTURA_PISO

        def update(self):
            self.rect[0] -= VELOCIDADE_JOGO

    class Cano(pygame.sprite.Sprite):
        def __init__(self, invertido, xpos, ytamanho):
            pygame.sprite.Sprite.__init__(self)

            self.image = pygame.image.load('assets/pipe-red.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (LARGURA_CANO , ALTURA_CANO))

            self.rect = self.image.get_rect()
            self.rect[0] = xpos

            self.rect[1] = ALTURA_TELA - ytamanho

            if invertido:
                self.image = pygame.transform.flip(self.image, False, True)
                self.rect[1] = - (self.rect[3] - ytamanho)

            self.mask = pygame.mask.from_surface(self.image)

        def update(self):
            self.rect[0] -= VELOCIDADE_JOGO

    def fora_tela(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def canos_aleatorios(xpos):
        tamanho = random.randint(200, 500)
        cano = Cano(False, xpos, tamanho)
        cano_invertido = Cano(True, xpos, ALTURA_TELA - tamanho - ESPACO_FALTANTE_CANO)

        return(cano, cano_invertido)

    # VARIÁVEIS FIXAS
    LARGURA_TELA = 400
    ALTURA_TELA = 800

    VELOCIDADE_JOGO = 10
    VELOCIDADE_PASSARO = 10
    GRAVIDADE_PASSARO = 1

    LARGURA_PISO = 2 * LARGURA_TELA
    ALTURA_PISO = 100

    LARGURA_CANO = 80
    ALTURA_CANO = 500
    ESPACO_FALTANTE_CANO = 200

    pygame.init()
    pygame.font.init()

    tela = pygame.display.set_mode ((LARGURA_TELA, ALTURA_TELA))

    FUNDO = pygame.image.load('assets/background-night.png')
    FUNDO = pygame.transform.scale(FUNDO,(LARGURA_TELA, ALTURA_TELA))
    PONTUACAO = pygame.font.SysFont('arial', 30)

    # PASSARO
    grupo_passaros = pygame.sprite.Group()
    passaro = Passaro()
    grupo_passaros.add(passaro)

    # PISO
    grupo_pisos = pygame.sprite.Group()

    for i in range(2):
        ground = Piso(LARGURA_PISO * i)
        grupo_pisos.add(ground)

    # CANO
    grupo_canos = pygame.sprite.Group()

    # PONTOS_INICIAIS
    pontos = 0

    for i in range(2):
        canos = canos_aleatorios(LARGURA_TELA * i + 800)

        grupo_canos.add(canos[0]) # CANO NORMAL
        grupo_canos.add(canos[1]) # CANO INVERTIDO

    clock = pygame.time.Clock()

    # GAME LOOP
    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    passaro.voar()

        tela.blit(FUNDO, (0, 0))

        if fora_tela(grupo_pisos.sprites()[0]):
            grupo_pisos.remove(grupo_pisos.sprites()[0])

            novo_piso = Piso(LARGURA_PISO - 20)
            grupo_pisos.add(novo_piso)

        if fora_tela(grupo_canos.sprites()[0]):
            grupo_canos.remove(grupo_canos.sprites()[0])
            grupo_canos.remove(grupo_canos.sprites()[0])

            canos = canos_aleatorios(LARGURA_TELA * 2)

            grupo_canos.add(canos[0]) # CANO NORMAL
            grupo_canos.add(canos[1]) # CANO INVERTIDO
            pontos += 1

        grupo_passaros.update()
        grupo_pisos.update()
        grupo_canos.update()

        grupo_passaros.draw(tela)
        grupo_canos.draw(tela)
        grupo_pisos.draw(tela)

        tela_pontos = PONTUACAO.render(f"Pontuação: {pontos}", 1, (255, 255, 255))

        tela.blit(tela_pontos, (0, 0))

        pygame.display.update()

        # GAMEOVER
        if (pygame.sprite.groupcollide(grupo_passaros, grupo_pisos, False, False, pygame.sprite.collide_mask) or
        pygame.sprite.groupcollide(grupo_passaros, grupo_canos, False, False, pygame.sprite.collide_mask)):
            break

if __name__ == "__main__":
    main()