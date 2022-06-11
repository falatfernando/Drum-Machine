from cgitb import grey
from operator import truediv
from tkinter import EventType
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
grey = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

#making the window structure
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Dinho's Drum Machine")
label_font = pygame.font.Font('freesansbold.ttf', 32) #change fonts?

fps  = 60
timer = pygame.time.Clock()
beats = 8 #tranform into user tempo input
rows = 8
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(rows)]
bpm = 240
playing = True
active_lenght = 0
active_beat = 0
beat_changed = True

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, HEIGHT - 100, WIDTH, 100], 5)
    boxes = []
    color = [grey, white, grey]

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
        pygame.draw.line(screen, grey, (0, (i * 75) + 75 ), (200, (i * 75) + 75), 3)

    for i in range(beats):
        for j in range(rows):
            #change the colors of active lines on rows
            if clicked[j][i] == -1:
                color = grey
            else:
                color = green
            # Always give largest possible beat equally divided
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j*75) + 5, ((WIDTH - 200) // beats) - 10, (((HEIGHT - 75)/rows)) - 10], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j*75), ((WIDTH - 200) // beats), (((HEIGHT - 75)/rows))], 5, 5) 
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j*75), ((WIDTH - 200) // beats), (((HEIGHT - 75)/rows))], 2, 5) 
            boxes.append((rect, (i, j)))
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200)//beats) + 200, 0, ((WIDTH - 200)//beats), rows * 75], 5, 3)
    return boxes

#main game loop
run = True
while run:
    timer.tick(fps) #use THIS framerate on math part
    screen.fill(black)
    boxes = draw_grid(clicked, active_beat)

    #event handling - check mouse/keyboard clicks and movements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #collision detection, doing this to further be able to diff clicked boxes by color
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1 
    
    #making movement to the beat tracker
    beat_lenght = 3600 // bpm #this is actually not 240 bpm should be 800 // bpm, need to calculate better

    if playing:
        if active_lenght < beat_lenght:
            active_lenght += 1
        else:
            active_lenght = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True
            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
    
pygame.quit()