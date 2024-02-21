import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 600
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 40)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))


# Definicja ścieżki do folderu z obrazami
IMAGE_PATH = "animation"

# Lista nazw plików z obrazami gracza
PLAYER_IMAGES = os.listdir(IMAGE_PATH)





# Load game background
background = pygame.transform.scale(pygame.image.load('./images/background.png'), (WIDTH, HEIGHT))
background_X1 = 0
background_X2 = background.get_width()
background_move = 2

# Create start button
start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)


# Create exit button
exit_button_rect = pygame.Rect(WIDTH - 50, 30, 40, 40)

# Load player image
player = pygame.image.load('./images/player.png').convert_alpha()
player_rect = player.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Game variables
score = 0
playing = False

def create_enemy():
    enemy_size = (50, 20)
    enemy = pygame.image.load('./images/enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy, enemy_size)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - enemy_size[1]), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

def create_bonus():
    bonus_size = (80, 100)
    bonus = pygame.image.load('./images/bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, bonus_size)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus_size[0]), 0, *bonus_size)
    bonus_move = [0, random.randint(1, 5)]
    return [bonus, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 150)

bonuses = []
enemies = []

image_index = 0  # Definiujemy początkową wartość dla zmiennej image_index

while True:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if start_button_rect.collidepoint(mouse_pos) and not playing:
                playing = True
                # Reset game variables
                player_rect.center = (WIDTH // 2, HEIGHT // 2)
                score = 0
                enemies = []  # Usuwamy wszystkie przeciwników po rozpoczęciu nowej gry
                bonuses = []  # Usuwamy wszystkie bonusy po rozpoczęciu nowej gry
                image_index = 0  # Resetujemy zmienną image_index
            elif exit_button_rect.collidepoint(mouse_pos) and not playing:
                pygame.quit()
                quit()
        elif event.type == CREATE_ENEMY and playing:
            enemies.append(create_enemy())
        elif event.type == CREATE_BONUS and playing:
            bonuses.append(create_bonus())
        elif event.type == CHANGE_IMAGE and playing:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0


    if not playing:
        main_display.blit(background, (0, 0))
        pygame.draw.rect(main_display, COLOR_BLUE, start_button_rect)
        start_text = FONT.render("Start", True, COLOR_WHITE)
        main_display.blit(start_text, start_button_rect.topleft)
        pygame.draw.rect(main_display, COLOR_RED, exit_button_rect)
        exit_text = FONT.render("X", True, COLOR_WHITE)
        main_display.blit(exit_text, exit_button_rect.topleft)
        pygame.display.flip()
        continue

    background_X1 -= background_move
    background_X2 -= background_move

    if background_X1 < -background.get_width():
        background_X1 = background.get_width()

    if background_X2 < -background.get_width():
        background_X2 = background.get_width()

    main_display.blit(background, (background_X1, 0))
    main_display.blit(background, (background_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move([0, 4])

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move([4, 0])

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move([0, -4])

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move([-4, 0])

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
