import pygame
import random

# Game window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Cloud Invaders")

# Set up the game clock
clock = pygame.time.Clock()

# Set up game objects
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 20:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)
            self.speedx = random.randrange(-2, 2)

class Lightning(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 30))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Set up Sprite Groups
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create game objects and add them to Sprite Groups
for i in range(8):
    c = Cloud()
    all_sprites.add(c)
    clouds.add(c)
for i in range(3):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

# Set up the player
player_image = pygame.Surface((50, 40))
player_image.fill(RED)
player_rect = player_image.get_rect()
player_rect.centerx = SCREEN_WIDTH / 2
player_rect.bottom = SCREEN_HEIGHT - 10

# Set up game variables
score = 0
game_over = False

# Main game loop
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Lightning(player_rect.centerx, player_rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)

    # Update game objects
    all_sprites.update()

    # Check for collisions between bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)
        score += 10

    # Check for collisions between player and enemies
    hits = pygame.sprite.spritecollide(player_rect, enemies, False)
    if hits:
        game_over = True

    # Draw game objects to the screen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.draw.rect(screen, WHITE, player_rect)
    pygame.display.flip()

    # Set the game clock
    clock.tick(60)

# Game over screen
pygame.quit()
