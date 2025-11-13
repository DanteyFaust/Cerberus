import pygame
import os

SPACE_IMAGE = pygame.image.load(os.path.join("./assets", "space.jpg"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("./assets", "spaceship_red.jpg"))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("./assets", "spaceship_yellow.jpg"))

WIDTH = 700
HEIGHT = 400

SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_WIDTH)), 90)
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_WIDTH)), 270)

pygame.init()

red = pygame.Rect(100, 150, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow = pygame.Rect(500, 150, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

SPACE_BG = pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10, HEIGHT)

VELOCITY = 1
FPS = 60
clock = pygame.time.Clock()

red_health = 10
yellow_health = 10
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

red_bullets = []
yellow_bullets = []
MAX_BULLETS = 3
BULLET_VEL = 7

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VELOCITY > 0:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_d] and red.x + VELOCITY + red.width < BORDER.x:
        red.x += VELOCITY
    if keys_pressed[pygame.K_w] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_s] and red.y + VELOCITY + red.height < HEIGHT:
        red.y += VELOCITY

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VELOCITY > BORDER.x + BORDER.width:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VELOCITY + yellow.width < WIDTH:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_UP] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and yellow.y + VELOCITY + yellow.height < HEIGHT:
        yellow.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets[:]:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets[:]:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    screen.blit(SPACE_BG, (0,0))
    
    # Здоровье
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, "white")
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, "white")
    screen.blit(red_health_text, (10, 10))
    screen.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))
    
    # Граница и корабли
    pygame.draw.rect(screen, 'white', BORDER)
    screen.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    screen.blit(RED_SPACESHIP, (red.x, red.y))
    
    # Пули
    for bullet in red_bullets:
        pygame.draw.rect(screen, 'red', bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, 'yellow', bullet)
    
    pygame.display.update()

def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, "white")
    screen.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)  # Задержка 3 секунды перед перезапуском

running = True
game_over = False
winner_text = ""

while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                red_bullets.append(bullet)
            
            if event.key == pygame.K_RETURN and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(yellow.x - 10, yellow.y + yellow.height//2 - 2, 10, 5)
                yellow_bullets.append(bullet)
        
        # Обработка событий попадания
        if event.type == RED_HIT:
            red_health -= 1
        
        if event.type == YELLOW_HIT:
            yellow_health -= 1
    
    # Проверка условий победы
    if red_health <= 0:
        winner_text = "YELLOW WINS!"
        game_over = True
    elif yellow_health <= 0:
        winner_text = "RED WINS!"
        game_over = True
    
    # Если игра окончена, показываем экран победы и перезапускаем
    if game_over:
        draw_winner(winner_text)
        # Сброс игры
        red_health = 10
        yellow_health = 10
        red_bullets.clear()
        yellow_bullets.clear()
        red.x = 100
        red.y = 150
        yellow.x = 500
        yellow.y = 150
        game_over = False
        continue
    
    # Основной игровой процесс
    if not game_over:
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)


pygame.quit()
