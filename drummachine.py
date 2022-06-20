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

# Load in sounds
hi_hat = mixer.Sound('sounds\hi hat.wav')
open_hat = mixer.Sound('sounds\open hat.wav')
snare = mixer.Sound('sounds\snare.wav')
clap = mixer.Sound('sounds\clap.wav')
kick = mixer.Sound('sounds\kick.wav')
eight = mixer.Sound('sounds\808.wav')
crash = mixer.Sound('sounds\crash.wav')
laugh = mixer.Sound('sounds\laugh.wav')

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1:
            if i == 0:
                hi_hat.play()
            if i == 1:
                open_hat.play()
            if i == 2:
                snare.play()
            if i == 3:
                clap.play()
            if i == 4:
                kick.play()
            if i == 5:
                eight.play()
            if i == 6:
                crash.play()
            if i == 7:
                laugh.play()                                                                                                

def draw_grid(clicks, beat):
    left_box = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, HEIGHT - 100, WIDTH, 100], 5)
    boxes = []
    color = [grey, white, grey]

    #Rows/Instruments Text
    hi_hat_text = label_font.render('Hi Hat', True, white)
    screen.blit(hi_hat_text, (20, 30))

    openhat_text = label_font.render('Open Hat', True, white)
    screen.blit(openhat_text, (20, 105))

    snare_text = label_font.render('Snare', True, white)
    screen.blit(snare_text, (20, 180))

    clap_text = label_font.render('Clap', True, white)
    screen.blit(clap_text, (20, 255))

    kick_text = label_font.render('Kick', True, white)
    screen.blit(kick_text, (20, 330))

    eight_text = label_font.render('808', True, white)
    screen.blit(eight_text, (20, 405))

    crash_text = label_font.render('Crash', True, white)
    screen.blit(crash_text, (20, 480))

    laugh_text = label_font.render('Laugh', True, white)
    screen.blit(laugh_text, (20, 555)) 

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

    if beat_changed:
        play_notes()
        beat_changed = False

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
    beat_lenght = 3200 // bpm #this is actually not 240 bpm!!! Should be multiples of ((800) // bpm) - check metronome

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