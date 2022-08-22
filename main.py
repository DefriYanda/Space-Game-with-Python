import pygame
import math
import random
from pygame import mixer

pygame.init()

# FPS
clock = pygame.time.Clock()
fps = 90

lebar = 800
tinggi = 600
window = pygame.display.set_mode((lebar,tinggi))
pygame.display.set_caption("Space Game")

# Logo
logo = pygame.image.load("img/logo.png")
pygame.display.set_icon(logo)

# Background
bg = pygame.image.load("img/bg.jpg")

# Player
playerImg = pygame.image.load("img/player.png")
player_x = (lebar // 2) - 32
player_y = 500
player_move = 0
player_speed = 4

# Enemy
enemyImg = []
enemy_x = []
enemy_y = []
move_enemy = []
enemy_move_x = []
enemy_move_y = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load("img/enemy.png"))
    enemy_x.append(random.randint(0,lebar - 64))
    enemy_y.append(random.randint(0,70))
    move_enemy.append([3,-3])
    enemy_move_x.append(random.choice(move_enemy[i]))
    enemy_move_y.append(35)

# Bullet 
bulletImg = pygame.image.load("img/laser.png")
bullet_x = 0
bullet_y = 490
bullet_move_x = 0
bullet_move_y = 7
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

score_x = 10
score_y = 10

# Game Over
over_text = pygame.font.Font("freesansbold.ttf",64)

# Background sound
mixer.music.load('sound/background.wav')
mixer.music.play()

# Functions
def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    window.blit(score,(x,y))

def show_over():
    game_over = over_text.render("GAME OVER",True,(255,255,255))
    window.blit(game_over,(200,250))

def player(x,y):
    window.blit(playerImg,(x,y))

def enemy(x,y,i):
    window.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImg,(x,y))

def is_collision(enemy_x,enemy_y,bullet_x,bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2) + (math.pow(enemy_y - bullet_y, 2))))
    if distance <= 40:
        return True
    else:
        return False

# Looping
run = True
while run:

    clock.tick(fps)

    window.fill((0,0,0))

    # Background
    window.blit(bg,(0,0))

    # Player dan enemy
    player(player_x,player_y)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move = -player_speed
            if event.key == pygame.K_RIGHT:
                player_move = player_speed
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('sound/laser.wav')
                    mixer.Sound.play(bullet_sound)
                    bullet_x = player_x + 15
                    fire_bullet(bullet_x,bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_move = 0

    # Player cek kiri kanan
    player_x += player_move
    if player_x <= 0:
        player_x = 0
    if player_x >= lebar - 64:
        player_x = lebar - 64

    for i in range(num_of_enemy):
        # Game Over
        if enemy_y[i] > 300:
            for j in range(num_of_enemy):
                enemy_y[i] = 2000
            show_over()
            break

        # Enemy Moving
        enemy_x[i] += enemy_move_x[i]
        if enemy_x[i] <= 0:
            enemy_move_x[i] = 3
            enemy_y[i] += enemy_move_y[i]
        if enemy_x[i] >= lebar - 64:
            enemy_move_x[i] = -3
            enemy_y[i] += enemy_move_y[i]
            
        # Collision
        collision = is_collision(enemy_x[i],enemy_y[i],bullet_x,bullet_y)
        if collision:
            explosion_sound = mixer.Sound('sound/explosion.wav')
            mixer.Sound.play(explosion_sound)
            bullet_y = 490
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0,lebar - 64)
            enemy_y[i] = random.randint(0,70)
            move_enemy[i] = [3,-3]
            enemy_move_x[i] = random.choice(move_enemy[i])

        enemy(enemy_x[i],enemy_y[i],i)

    # Show Score
    show_score(score_x,score_y)

    # Bullet moving
    if bullet_y <= 0:
        bullet_state = "ready"
        bullet_y = 490

    if bullet_state is "fire":
        fire_bullet(bullet_x,bullet_y)
        bullet_y -= bullet_move_y

    pygame.display.update()

pygame.quit()