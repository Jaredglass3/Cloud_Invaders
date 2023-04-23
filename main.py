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
        self.speed = random.randint(1, 5)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()

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
        if self.rect.bottom < 0:
            self.kill()

class Game:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(WIDTH//2, HEIGHT-50)
        self.all_sprites.add(self.player)

        for i in range(10):
            self.create_enemy()

    def create_enemy(self):
        enemy = Enemy(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)
                        shoot_sound.play()

            self.all_sprites.update()

            hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
            for hit in hits:
                self.create_enemy()
                self.score += 1
                explosion_sound.play()

            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                game_over_sound.play()
                running = False

            screen.fill((0, 0, 0))
            screen.blit(pygame.image.load('background_sprite.png').convert(), (0, 0))

            self.all_sprites.draw(screen)

            score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
