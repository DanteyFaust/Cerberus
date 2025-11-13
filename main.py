import pygame
import os
SPACE_IMAGE = pygame.image.load(os.path.join("./assets", "space.jpg"))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("./assets", "spaceship_red.jpg"))
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("./assets", "spaceship_yellow.jpg"))

WIDTH = 600
HEIGHT = 300

SPACESHIP_WIDHT = 55
SPACESHIP_HEIGHT = 40

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDHT, SPACESHIP_WIDHT)), 90)
pygame.init()
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDHT, SPACESHIP_WIDHT)), 270)
pygame.init()

red = pygame.Rect(100, 150,  SPACESHIP_WIDHT, SPACESHIP_HEIGHT)
yellow = pygame.Rect(500, 150,  SPACESHIP_WIDHT, SPACESHIP_HEIGHT)

SPACE_BG= pygame.transform.scale(SPACE_IMAGE, (WIDTH, HEIGHT))

screen = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH/2 - 5, 0 , 10, HEIGHT)

VELOCITY = 1

FPS = 60

clock= pygame.time.Clock()

red_health = 10
yellow_health = 10
HEALTH_FONT = pygame.font.SysFont('comicsans', 20)

red_bullets = []
yellow_bullets = []
MAX_BULLETS = 3
BULLET_VEL= 7 

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VELOCITY > 0:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_d] and red.x + VELOCITY + red.width < BORDER.x:
        red.x += VELOCITY
    if keys_pressed[pygame.K_w] and red.y - VELOCITY  > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_s] and red.y + VELOCITY + red.width < HEIGHT - 15:
        red.y += VELOCITY

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VELOCITY > BORDER.x + BORDER.width:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VELOCITY + yellow.width < WIDTH:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_UP] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:
        yellow.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.pygame.Rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.pygame.sprite.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.pygame.Rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.pygame.sprite.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


while True:
    clock.tick(FPS)
    screen.blit(SPACE_BG, (0,0))
    red_health_text = HEALTH_FONT.render("Health:" + str(red_health), 1, "white")
    yellow_health_text = HEALTH_FONT.render("Health:" + str(yellow_health), 1, "white")
    screen.blit(red_health_text, (10, 10))
    screen.blit(yellow_health_text, (WIDTH - red_health_text.get_width()-10, 10))
    pygame.draw.rect(screen, 'white', BORDER)
    screen.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    screen.blit(RED_SPACESHIP, (red.x, red.y))
    keys_pressed = pygame.key.get_pressed()
    red_handle_movement(keys_pressed, red)
    yellow_handle_movement(keys_pressed, yellow)
    for bullet in red_bullets:
        pygame.draw.rect(screen, 'red', bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, 'yellow', bullet)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10 , 5)
                red_bullets.append(bullet)

                if event.key == pygame.K_RETURN and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height/2 - 2, 10, 5)
                yellow_bullets.append(bullet)


            


        pygame.display.update()