import pygame
import random
from pygame.locals import *
from enum import Enum

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.direction = 1

    def update(self):
        self.rect.move_ip(0, self.speed)
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.move_ip(0, self.speed)

class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.y < 0:
            self.kill()

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

# Game state enum
class GameState(Enum):
    PLAYING = 0
    GAME_OVER = 1
    VICTORY = 2

# Initialize game state
game_state = GameState.PLAYING

# Main game loop
while game_state == GameState.PLAYING:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_SPACE:
            lightning = Lightning(player.rect.x + 22, player.rect.y)
            all_sprites.add(lightning)
            lightning_bolts.add(lightning)

    # Update all sprites
    all_sprites.update()

    # Collision detection
    pygame.sprite.groupcollide(enemies, lightning_bolts, True, True)

    # Check for victory
    if len(enemies) == 0:
        game_state = GameState.VICTORY

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

if game_state == GameState.VICTORY:
    print("You won!")
else:
    print("Game Over.")
