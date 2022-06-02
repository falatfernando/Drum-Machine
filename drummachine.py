from cgitb import grey
from turtle import width
import pygame
from pygame import mixer

pygame.init()

#experiment other sizes - maybe be flexible to other resolutions?
WIDTH = 1400 
HEIGHT = 700

#experiment other colors
black = (0, 0, 0) 
white = (255, 255, 255) 
gray = (128, 128, 128) 

#making the window structure
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Dinho's Drum Machine")
label_font = pygame.font.Font('freesansbold.ttf', 32) #change fonts?

fps  = 60
timer = pygame.time.Clock()
beats = 8 #tranform into user tempo input
rows = 8

def draw_grid():
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 100, WIDTH, 100], 5)
    boxes = []
    color = [grey, white, gray]

    #Rows/Instruments Text (hh snare kick tom floor china crash clap)
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (20, 30))
    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (20, 105))
    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (20, 180))
    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (20, 255))
    china_text = label_font.render('China', True, white)
    screen.blit(china_text, (20, 330))
    tom_text = label_font.render('Tom', True, white)
    screen.blit(tom_text, (20, 405))
    floor_tom_text = label_font.render('Floor Tom', True, white)
    screen.blit(floor_tom_text, (20, 480))
    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (20, 555))

    # Drawing grid
    for i in range(rows):
        pygame.draw.line(screen, gray, (0, (i * 75) + 75 ), (200, (i * 75) + 75), 3)

    for i in range(beats):
        for j in range(rows):
            # Always give largest possible beat equally divided
            rect = pygame.draw.rect(screen, gray, [i * ((WIDTH - 200) // beats) + 200, (j*75), ((WIDTH - 200) // beats), (((HEIGHT - 75)/rows))], 5, 5) 

#main game loop
run = True
while run:
    timer.tick(fps) #use THIS framerate on math part
    screen.fill(black)
    draw_grid()
    #event handling - check mouse/keyboard clicks and movements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()

pygame.quit()