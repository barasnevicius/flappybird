import pygame
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/yellowbird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/yellowbird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]

        self.speed += GRAVITY

        # UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

class Ground(pygame.sprite.Sprite):
    def __init__(self, width, height, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/base.png')
        self.image = pygame.transform.scale(self.image, (width , height))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - height

    def update(self):
        self.rect[0] -= GAME_SPEED

pygame.init()
screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('assets/background-night.png')
BACKGROUND = pygame.transform.scale(BACKGROUND,(SCREEN_WIDTH, SCREEN_HEIGHT))

# BIRD
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

# FLOOR
ground_group = pygame.sprite.Group()

for i in range(2):
    ground = Ground(2 * SCREEN_WIDTH, 100, 2 * SCREEN_WIDTH * i)
    ground_group.add(ground)

clock = pygame.time.Clock()

# GAME LOOP
while True:
    clock.tick(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND,(0,0))

    bird_group.update()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()