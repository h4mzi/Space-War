import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900,500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space War")

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join(
    'C:\\Users\\Gaming\\Documents\\Space War\\oof.mp3'))
BULLET_FIRE_SOUND=pygame.mixer.Sound(os.path.join(
    'C:\\Users\\Gaming\\Documents\\Space War\\beep.mp3'))

WHITE=(255, 255, 255)
BLACK=(0, 0, 0)
GREEN=(0, 255, 0)
RED=(255, 0, 0)
PINK=(255, 192, 203)
AQUA=(115, 253, 221)

HEALTH_FONT=pygame.font.SysFont('Garamond', 40)
WINNER_FONT=pygame.font.SysFont('Simplified Arabic Fixed Regular', 55)

BULLET_VEL=8
MAX_BULLETS=3

ALIEN_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

FPS = 60
VEL=4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55 , 30
BORDER=pygame.Rect(WIDTH//2-5, 0, 4, HEIGHT)


RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join(
    'C:\\Users\\Gaming\\Documents\\Space War\\redship.png'))
RED_SPACESHIP=pygame.transform.rotate(RED_SPACESHIP_IMAGE, 270)

ALIEN_SPACESHIP_IMAGE=pygame.image.load(os.path.join(
    'C:\\Users\\Gaming\\Documents\\Space War\\aleinship.png'))
ALIEN_SPACESHIP=pygame.transform.rotate(ALIEN_SPACESHIP_IMAGE, 90)

EARTH=pygame.transform.scale(pygame.image.load(os.path.join(
    'C:\\Users\\Gaming\\Documents\\Space War\\earth.jpg')), (WIDTH, HEIGHT))


def RED_HANDLE(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x-VEL>0: #left
        red.x-=VEL
    if keys_pressed[pygame.K_d] and red.x-VEL+red.width<BORDER.x:#right
        red.x+=VEL
    if keys_pressed[pygame.K_w] and red.y-VEL>0:#up
        red.y-=VEL
    if keys_pressed[pygame.K_s] and red.y-VEL+red.height<HEIGHT-30:#down
        red.y+=VEL

def ALIEN_HANDLE(keys_pressed, alien):
    if keys_pressed[pygame.K_UP] and alien.y-VEL>0:
        alien.y-=VEL
    if keys_pressed[pygame.K_DOWN] and alien.y-VEL+ alien.height<HEIGHT-20:
        alien.y+=VEL
    if keys_pressed[pygame.K_LEFT] and alien.x-VEL> BORDER.x + BORDER.width:
        alien.x-=VEL
    if keys_pressed[pygame.K_RIGHT] and alien.x-VEL+ alien.width<WIDTH:
        alien.x+=VEL

def handle_bullets(alien_bullets, red_bullets, alien, red):
    for bullet in alien_bullets:
        bullet.x-=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            alien_bullets.remove(bullet)
        elif bullet.x<0:
            alien_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x+=BULLET_VEL
        if alien.colliderect(bullet):
            pygame.event.post(pygame.event.Event(ALIEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.x>WIDTH:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text=WINNER_FONT.render(text, 1, AQUA)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /2,
                          HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)

def drawwindow(red, alien, red_bullets, alien_bullets, red_health, alien_health):
    WIN.blit(EARTH, (0, 0))
    pygame.draw.rect(WIN, PINK, BORDER)
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    WIN.blit(ALIEN_SPACESHIP,(alien.x,alien.y))
    red_health_text=HEALTH_FONT.render("Health:" + str(red_health), 1, WHITE)
    alien_health_text=HEALTH_FONT.render("Health:" + str(alien_health), 1, WHITE)
    WIN.blit(alien_health_text, (WIDTH-red_health_text.get_width()-10, 10))
    WIN.blit(red_health_text, (10,10))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    
    for bullet in alien_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def main():
    red=pygame.Rect(20, 220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    alien=pygame.Rect(830, 220, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets=[]
    alien_bullets=[]
    
    red_health=10
    alien_health=10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets)< MAX_BULLETS:
                    bullet= pygame.Rect(red.x, red.y+ red.height//2-2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(alien_bullets)< MAX_BULLETS:
                    bullet= pygame.Rect(alien.x + alien.width, alien.y+ alien.height//2-2, 10, 5)
                    alien_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()
            if event.type==ALIEN_HIT:    
                alien_health-=1
                BULLET_HIT_SOUND.play()
        
        winner_text=""
        if red_health<=0:
            winner_text="Aliens have taken over the world, thanks to you !"
        if alien_health<=0:
            winner_text="""Congrats,You just saved the world ! """
        if winner_text!="":
            draw_winner(winner_text)
            break

        keys_pressed=pygame.key.get_pressed()
        RED_HANDLE(keys_pressed, red)
        ALIEN_HANDLE(keys_pressed, alien)
        handle_bullets(alien_bullets, red_bullets, alien, red)
        drawwindow(red, alien, red_bullets, alien_bullets, red_health, alien_health)
    
    main()

if __name__ == "__main__":
    main()