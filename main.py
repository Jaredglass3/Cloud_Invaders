import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cloud Invaders")

# Load the cloud and enemy images
cloud_image = pygame.image.load('cloud.png')
enemy_image = pygame.image.load('enemy.png')

# Create the player object
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cloud_image
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = 5

# Create the enemy objects
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

# Create a group for the enemies
enemies = pygame.sprite.Group()
for i in range(10):
    enemy = Enemy()
    enemies.add(enemy)
