import pygame
import random
import sys
from pygame.locals import *
from enum import Enum

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load sounds
shoot_sound = pygame.mixer.Sound('shoot.wav')
explosion_sound = pygame.mixer.Sound('explosion.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# Load background music and play it in a loop
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('player_sprite.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('enemy_sprite.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 0.25
        self.direction = 1

    def update(self):
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.move_ip(0, self.speed * 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('bullet_sprite.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.y < 0:
            self.kill()

# Create player and sprite groups
player = Player(WIDTH // 2, HEIGHT - 50)
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Create a 10x10 grid of enemies
ENEMY_SPACING = 80
for i in range(10):
    for j in range(10):
        enemy = Enemy(ENEMY_SPACING * i, ENEMY_SPACING * j)
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
            shoot_sound.play()
            bullet = Bullet(player.rect.x + 22, player.rect.y)
            all_sprites.add(bullet)
            bullets.add(bullet)

    # Update all sprites
    all_sprites.update()

    # Collision detection
    collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
    if collisions:
        explosion_sound.play()

    # Check for victory
    if len(enemies) == 0:
        game_state = GameState.VICTORY

    # Check for game over
    if pygame.sprite.spritecollideany(player, enemies):
        game_over_sound.play()
        game_state = GameState.GAME_OVER

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

if game_state == GameState.VICTORY:
    print("You won!")
else:
    print("Game Over.")
