import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cloud Invaders")

# Set up assets
BACKGROUND = pygame.image.load("assets/background.png").convert()
PLAYER_IMG = pygame.image.load("assets/player.png").convert_alpha()
ENEMY_IMG = pygame.image.load("assets/enemy.png").convert_alpha()
LIGHTNING_IMG = pygame.image.load("assets/lightning.png").convert_alpha()

# Set up clock
clock = pygame.time.Clock()

# Custom classes
class Player(pygame.sprite.Sprite):
    # ... (Same as before)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.move_ip(0, self.speed)

class Lightning(pygame.sprite.Sprite):
    # ... (Same as before)

# Create player and sprite groups
player = Player(WIDTH // 2, HEIGHT - 50, 50, 50)
enemies = pygame.sprite.Group()
lightning_bolts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create a 10x10 grid of enemies
ENEMY_SPACING = 80
for i in range(10):
    for j in range(10):
        enemy = Enemy(ENEMY_SPACING * i, ENEMY_SPACING * j, 50, 50)
        all_sprites.add(enemy)
        enemies.add(enemy)

# Main game loop
running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                lightning = Lightning(player.rect.x + player.rect.width // 2 - 5, player.rect.y)
                all_sprites.add(lightning)
                lightning_bolts.add(lightning)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    for lightning in lightning_bolts:
        lightning.update()
        hit_enemies = pygame.sprite.spritecollide(lightning, enemies, True)
        if hit_enemies:
            lightning.kill()

    for enemy in enemies:
        enemy.update()
        if pygame.sprite.collide_rect(player, enemy):
            running = False
            print("Player was hit!")

    screen.blit(BACKGROUND, (0, 0))
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    pygame.display.flip()

pygame.quit()