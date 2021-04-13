import pygame
import os

#https://github.com/dkruchinin/spdemo/blob/master/spdemo.py

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH, HEIGHT = 1280, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
VELOCITY = 3
BULLET_VEL = 10
MAX_BULLET = 3

ROCKET1_HIT = pygame.USEREVENT+1
ROCKET2_HIT = pygame.USEREVENT+2

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

SPACESHIP_IMG1 = pygame.image.load("rocket1.png")
SPACESHIP_IMG2 = pygame.image.load("rocket2.png")
SPACE_IMG = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))

SPACESHIP1 = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG1, (64, 64)), -45)
SPACESHIP2 = pygame.transform.rotate(pygame.transform.scale(SPACESHIP_IMG2, (64, 64)), 135)

pygame.display.set_caption("Race")


def Rocket1Controller(keys_pressed, rocketRect1):
    # Left
    if keys_pressed[pygame.K_a] and rocketRect1.x - VELOCITY > 0:
        rocketRect1.x -= VELOCITY
    # Right
    if keys_pressed[pygame.K_d] and rocketRect1.x + VELOCITY + rocketRect1.width < BORDER.x - 5:
        rocketRect1.x += VELOCITY
    # Up
    if keys_pressed[pygame.K_w] and rocketRect1.y - VELOCITY > 0 - 24:
        rocketRect1.y -= VELOCITY
    # Down
    if keys_pressed[pygame.K_s] and rocketRect1.y + VELOCITY + rocketRect1.height < HEIGHT:
        rocketRect1.y += VELOCITY


def Rocket2Controller(keys_pressed, rocketRect2):
    # Left
    if keys_pressed[pygame.K_j]:
        rocketRect2.x -= 1
    # Right
    if keys_pressed[pygame.K_l]:
        rocketRect2.x += 1
    # Up
    if keys_pressed[pygame.K_i]:
        rocketRect2.y -= 1
    # Down
    if keys_pressed[pygame.K_k]:
        rocketRect2.y += 1


def draw_window(rocketRect1, rocketRect2, bullets1, bullets2):
    WIN.blit(SPACE_IMG, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(SPACESHIP1, (rocketRect1.x, rocketRect1.y))
    WIN.blit(SPACESHIP2, (rocketRect2.x, rocketRect2.y))

    for bullet in bullets1:
        pygame.draw.rect(WIN, BLACK, bullet)

    for bullet in bullets2:
        pygame.draw.rect(WIN, BLACK, bullet)
    pygame.display.update()

def handle_bullets(bullets1, bullets2, rocketRect1, rocketRect2):
    for bullet in bullets1:
        bullet.x += BULLET_VEL
        if rocketRect2.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ROCKET2_HIT))
            bullets1.remove(bullet)
        elif bullet.x > WIDTH:
            bullets1.remove(bullet)
    for bullet in bullets2:
        bullet.x -= BULLET_VEL
        if rocketRect1.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ROCKET1_HIT))
            bullets2.remove(bullet)
        elif bullet.x < 0:
            bullets2.remove(bullet)

def main():
    rocketRect1 = pygame.Rect(100, 300, 64, 64)
    rocketRect2 = pygame.Rect(700, 300, 64, 64)
    bullets1 = []
    bullets2 = []
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullets1) < MAX_BULLET:
                    bullet = pygame.Rect(rocketRect1.x + rocketRect1.width, rocketRect1.y + rocketRect1.height // 2 - 2,
                                         10, 5)
                    bullets1.append(bullet)
                if event.key == pygame.K_RCTRL and len(bullets2) < MAX_BULLET:
                    bullet = pygame.Rect(rocketRect2.x, rocketRect2.y + rocketRect2.height // 2 - 2,
                                         10, 5)
                    bullets2.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        Rocket1Controller(keys_pressed, rocketRect1)
        Rocket2Controller(keys_pressed, rocketRect2)
        handle_bullets(bullets1, bullets2, rocketRect1, rocketRect2)
        draw_window(rocketRect1, rocketRect2, bullets1, bullets2)
    pygame.quit()


if __name__ == "__main__":
    main()
