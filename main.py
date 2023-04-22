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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = LIGHTNING_IMG
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.y < -self.rect.height:
            self.kill()

# Create player and sprite groups
player = Player(WIDTH // 2, HEIGHT - 50, 50, 50)
enemies = pygame.sprite.Group()
lightning_bolts = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Main game loop
running = True
while running:
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                lightning = Lightning(player.rect.x + player.rect.width // 2, player.rect.y)
                lightning_bolts.add(lightning)
                all_sprites.add(lightning)

    # Update
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    lightning_bolts.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        print("Player was hit!")
        running = False

    # Spawn enemies
    if random.random() < 0.01:
        enemy = Enemy(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT // 2), 50, 50)
        enemies.add(enemy)
        all_sprites.add(enemy)

    # Draw
    screen.blit(BACKGROUND, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()