import pygame
import random
from pygame.locals import *
from enum import Enum

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
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = PLAYER_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5

    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1
        self.direction = 1

    def update(self):
        self.rect.move_ip(self.speed * self.direction, 0)
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1
            self.rect.move_ip(0, self.speed)

class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = LIGHTNING_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -5

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.y < 0:
            self.kill()

# Game state enum
class GameState(Enum):
    PLAYING = 0
    GAME_OVER = 1
    VICTORY = 2

# Initialize game state
game_state = GameState.PLAYING

# Main game loop
while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == KEYDOWN:
            if game_state == GameState.PLAYING:
                if event.key == K_SPACE:
                    lightning = Lightning(player.rect.x + player.rect.width // 2 - 5, player.rect.y)
                    all_sprites.add(lightning)
                    lightning_bolts.add(lightning)
            elif game_state in (GameState.GAME_OVER, GameState.VICTORY):
                if event.key == K_r:
                    # Restart the game
                    player = Player(WIDTH // 2, HEIGHT - 50, 50, 50)
                    enemies = pygame.sprite.Group()
                    lightning_bolts = pygame.sprite.Group()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(player)

                    for i in range(10):
                        for j in range(10):
                            enemy = Enemy(ENEMY_SPACING * i, ENEMY_SPACING * j, 50, 50)
                            all_sprites.add(enemy)
                            enemies.add(enemy)

                    game_state = GameState.PLAYING
                elif event.key == K_q:
                    pygame.quit()

    if game_state == GameState.PLAYING:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)

        for lightning in lightning_bolts:
            lightning.update()
            hit_enemies = pygame.sprite.spritecollide(lightning, enemies, True)
            if hit_enemies:
                lightning.kill()
                if not enemies:
                    print("All enemies defeated!")
                    game_state = GameState.VICTORY

        for enemy in enemies:
            enemy.update()
            if pygame.sprite.collide_rect(player, enemy):
                print("Player was hit!")
                game_state = GameState.GAME_OVER

        screen.blit(BACKGROUND, (0, 0))
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        pygame.display.flip()

    if game_state == GameState.GAME_OVER:
        # Display "Game Over" message and instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press
