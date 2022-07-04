from ast import While
from cProfile import label
from email.header import Header
from lib2to3.pygram import python_grammar_no_print_statement
from operator import truediv
from pydoc import cli
from tkinter import EventType
from turtle import width
import typing
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
dark_gray = (50, 50, 50)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

#making the window structure
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Dinho's Drum Machine")
label_font = pygame.font.Font('freesansbold.ttf', 32) #change fonts?
medium_font = pygame.font.Font('freesansbold.ttf', 16)

fps  = 60
timer = pygame.time.Clock()
beats = 8 #tranform into user tempo input
rows = 8
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(rows)]
active_list = [1 for _ in range(rows)]
bpm = 240
playing = True
active_lenght = 0
active_beat = 0
beat_changed = True
save_menu = False
load_menu = False

# Save file structure
saved_beats = []
file = open('my_beats.txt', 'r')
for line in file:
    saved_beats.append(line)
beat_name = ''
typing = False

# Load in sounds
hi_hat = mixer.Sound('sounds\hi hat.wav')
open_hat = mixer.Sound('sounds\open hat.wav')
snare = mixer.Sound('sounds\snare.wav')
clap = mixer.Sound('sounds\clap.wav')
kick = mixer.Sound('sounds\kick.wav')
eight = mixer.Sound('sounds\808.wav')
crash = mixer.Sound('sounds\crash.wav')
laugh = mixer.Sound('sounds\laugh.wav')
#set sound channels to above from 8
pygame.mixer.set_num_channels(rows * 3)

def play_notes():
    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
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

def draw_grid(clicks, beat, actives):
    left_box = pygame.draw.rect(screen, gray, [0, 0, 200, HEIGHT - 100], 5)
    bottom_box = pygame.draw.rect(screen, gray, [0, HEIGHT - 100, WIDTH, 100], 5)
    boxes = []
    color = [gray, white, gray]

    #Rows/Instruments Text
    hi_hat_text = label_font.render('Hi Hat', True, color[actives[0]])
    screen.blit(hi_hat_text, (20, 30))

    openhat_text = label_font.render('Open Hat', True, color[actives[1]])
    screen.blit(openhat_text, (20, 105))

    snare_text = label_font.render('Snare', True, color[actives[2]])
    screen.blit(snare_text, (20, 180))

    clap_text = label_font.render('Clap', True, color[actives[3]])
    screen.blit(clap_text, (20, 255))

    kick_text = label_font.render('Kick', True, color[actives[4]])
    screen.blit(kick_text, (20, 330))

    eight_text = label_font.render('808', True, color[actives[5]])
    screen.blit(eight_text, (20, 405))

    crash_text = label_font.render('Crash', True, color[actives[6]])
    screen.blit(crash_text, (20, 480))

    laugh_text = label_font.render('Laugh', True, color[actives[7]])
    screen.blit(laugh_text, (20, 555)) 

    # Drawing grid
    for i in range(rows):
        pygame.draw.line(screen, gray, (0, (i * 75) + 75 ), (200, (i * 75) + 75), 3)

    for i in range(beats):
        for j in range(rows):
            #change the colors of active lines on rows
            if clicked[j][i] == -1:
                color = gray
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = dark_gray
            # Always give largest possible beat equally divided
            rect = pygame.draw.rect(screen, color, [i * ((WIDTH - 200) // beats) + 205, (j*75) + 5, ((WIDTH - 200) // beats) - 10, (((HEIGHT - 75)/rows)) - 10], 0, 3)
            pygame.draw.rect(screen, gold, [i * ((WIDTH - 200) // beats) + 200, (j*75), ((WIDTH - 200) // beats), (((HEIGHT - 75)/rows))], 5, 5) 
            pygame.draw.rect(screen, black, [i * ((WIDTH - 200) // beats) + 200, (j*75), ((WIDTH - 200) // beats), (((HEIGHT - 75)/rows))], 2, 5) 
            boxes.append((rect, (i, j)))
        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200)//beats) + 200, 0, ((WIDTH - 200)//beats), rows * 75], 5, 3)
    return boxes

def draw_save_menu(beat_name, typing):
    pygame.draw.rect(screen, black,[0, 0,  WIDTH, HEIGHT])
    menu_text = label_font.render('Insert a name for your creation!', True, white)
    saving_btn = pygame.draw.rect(screen, gray, [WIDTH//2 - 200, HEIGHT * 0.75 + 80, 400, 50], 0 , 5)
    saving_text = label_font.render('Save Beat!', True, white)
    screen.blit(save_text, (WIDTH // 2 - 30, HEIGHT * 0.75 + 100))
    screen.blit(menu_text, (450, 75))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0 , 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    if typing:
        pygame.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0 , 5)
    entry_rect = pygame.draw.rect(screen, gray, [400, 200, 600, 200], 5 , 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, entry_rect

def draw_load_menu():
    pygame.draw.rect(screen, black,[0, 0,  WIDTH, HEIGHT])
    menu_text = label_font.render('Load one of your creations!', True, white)
    screen.blit(menu_text, (450, 75))
    exit_btn = pygame.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0 , 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    return exit_btn

#main game loop
run = True
while run:
    timer.tick(fps) #use THIS framerate on math part
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_list)
    # lower menu buttons
    play_pause = pygame.draw.rect(screen, gray, [30, HEIGHT - 80, 200, 60], 0, 5 )
    play_text = label_font.render('Play/Pause', True, white)
    screen.blit(play_text, (40, HEIGHT - 75))
    if playing:
        play_text_2 = medium_font.render("Playing", True, dark_gray)
    else:
        play_text_2 = medium_font.render("Paused", True, dark_gray)
    screen.blit(play_text_2, (150, HEIGHT - 40))

    # BPM Display
    bpm_rect = pygame.draw.rect(screen, gray, [300, HEIGHT-80, 200, 60], 5, 5)
    bpm_text = medium_font.render('BPM', True, white)
    screen.blit(bpm_text, (380, HEIGHT - 73))
    bpm_text_2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpm_text_2, (370, HEIGHT - 55))

    # Tempo changer
    bpm_add_rect = pygame.draw.rect(screen, gray, [570, HEIGHT - 85, 30, 30], 0 ,5)
    bpm_sub_rect = pygame.draw.rect(screen, gray, [570, HEIGHT - 45, 30, 30], 0 ,5)
    add_text = medium_font.render('+5', True, white)
    sub_text = medium_font.render('-5', True, white)
    screen.blit(add_text, (573, HEIGHT - 80)) # Find a way to center this
    screen.blit(sub_text, (573, HEIGHT - 40)) # Find a way to center this

    # Beats Display
    beats_rect = pygame.draw.rect(screen, gray, [670, HEIGHT-80, 200, 60], 5, 5)
    beats_text = medium_font.render('Beats', True, white)
    screen.blit(beats_text, (750, HEIGHT - 73))
    beats_text_2 = label_font.render(f'{beats}', True, white)
    screen.blit(beats_text_2, (765, HEIGHT - 55))

    # Beats changer
    beats_add_rect = pygame.draw.rect(screen, gray, [940, HEIGHT - 85, 30, 30], 0 ,5)
    beats_sub_rect = pygame.draw.rect(screen, gray, [940, HEIGHT - 45, 30, 30], 0 ,5)
    beats_add_text = medium_font.render('+1', True, white)
    beats_sub_text = medium_font.render('-1', True, white)
    screen.blit(beats_add_text, (945, HEIGHT - 80))
    screen.blit(beats_sub_text, (945, HEIGHT - 40))

    # Instrument controls
    instruments_rects = []
    for i in range(rows):
        rect = pygame.rect.Rect((0, i * 75), (200, 100))
        instruments_rects.append(rect)

    if beat_changed:
        play_notes()
        beat_changed = False

    # Save and load panel
    save_button = pygame.draw.rect(screen, gray, [1040, HEIGHT - 85, 100, 30])
    load_button = pygame.draw.rect(screen, gray, [1040, HEIGHT - 45, 100, 30])
    save_text = medium_font.render('Save Beat', True, white)
    load_text = medium_font.render('Load Beat', True, white)
    screen.blit(save_text, (1050, HEIGHT - 80))
    screen.blit(load_text, (1050, HEIGHT - 40))

    # Clear board panel
    clear_button = pygame.draw.rect(screen, gray, [1215, HEIGHT -80, 100, 60])
    clear_text = label_font.render('Clear', True, white)
    screen.blit(clear_text, (1220, HEIGHT - 65))

    # Menu options
    if save_menu:
        exit_button, saving_btn, entry_rectangle = draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button = draw_load_menu()

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

        if event.type == pygame.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause.collidepoint(event.pos):
                if playing:
                    playing = False
                elif not playing:
                    playing = True
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -=5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -=1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(rows)]
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True
            for i in range(len(instruments_rects)):
                if instruments_rects[i].collidepoint(event.pos):
                    active_list[i] *=-1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name = ''
                typing = False
            # Making typing beat name possible
            if entry_rectangle.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            elif saving_btn.collidepoint(event.pos):
                file = open('my_beats.txt', 'w')
                saved_beats.append(f'\n name: {beat_name}, beats: {beats}, bpm {bpm}, selected: {clicked}')
                for i in range(len(saved_beats)):
                    file.write(str(saved_beats[i]))
                file.close()
                save_menu = False
                typing = False
                beat_name = ''
        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

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