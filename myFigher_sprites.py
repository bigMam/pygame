import pygame
import random
import sys
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 700
# 初始化得分
score = 0

# Create a player sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width / 2, screen_height - self.rect.height)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x  > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < SCREEN_HEIGHT - self.rect.height:
            self.rect.y += self.speed

        hits = pygame.sprite.spritecollide(self, enemies, True)
        for hit in hits:
            game_over()

    def shoot(self):
        bullet = Bullet(self.rect.center)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Create an enemy sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("image/enemy.png")
        self.rect = self.image.get_rect()
        enemy_x_pos = random.randint(self.rect.width, screen_width - self.rect.width)
        self.rect.center = (enemy_x_pos, self.rect.height)
        self.speed = 3

        self.down_index = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()

# Create a bullet sprite
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("image/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = -6

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()


def show_score(score):
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def game_over():
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH/2 - game_over_text.get_width()/2, SCREEN_HEIGHT/2 - game_over_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()


explotion_image = pygame.image.load('image/ExplotionSheetColor.png')

explotion_surface = []
explotion_surface.append(explotion_image.subsurface(pygame.Rect(0,0,33,32)))
explotion_surface.append(explotion_image.subsurface(pygame.Rect(34,0,33,32)))
explotion_surface.append(explotion_image.subsurface(pygame.Rect(67,0,33,32)))

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = SCREEN_WIDTH
screen_height = SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the game
pygame.display.set_caption("飞机大战")

# Load the background image
background = pygame.image.load("image/background.png")

# Set the clock
clock = pygame.time.Clock()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemy_down_group = pygame.sprite.Group()

player_sprite = Player()
enemy_sprite = Enemy()

all_sprites.add(player_sprite, enemy_sprite)
enemies.add(enemy_sprite)

font = pygame.font.SysFont(None, 48)

ticks = 1
ANIMATE_CYCLE = 60

# Set the event loop
running = True
while running:
    ticks += 1
    # Draw the background
    screen.blit(background, (0, 0))

    if ticks > ANIMATE_CYCLE:
        ticks = 1

    # Set the FPS
    dt = clock.tick(60)

    # Set the event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player_sprite.shoot()
    if ticks % 50 == 0:
        enemy_sprite = Enemy()
        all_sprites.add(enemy_sprite)
        enemies.add(enemy_sprite)


    # Update all sprites
    all_sprites.update()

    enemy_down_group.add(pygame.sprite.groupcollide(enemies,bullets,True,True))
    for enemy_down in enemy_down_group:
        screen.blit(explotion_surface[enemy_down.down_index],(enemy_down.rect.centerx - 15, enemy_down.rect.centery - 16))
        if ticks % 2 == 0:
            if enemy_down.down_index < 2:
                enemy_down.down_index += 1
            else:
                enemy_down_group.remove(enemy_down)
                score += 1

    # Draw all sprites
    all_sprites.draw(screen)

    show_score(score)

    # Update the screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
sys.exit()
