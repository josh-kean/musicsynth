import sys, os
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
#class for playing a WAV file
class NotePlayer:
    def __init__(self, beat=1):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {} #dictionary of all possible notes
        self.beat = beat

    def add_notes(self, file_name):
        self.notes[file_name] = pygame.mixer.Sound(file_name)

    def quit_player(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
        return True

    def play_sequence(self, sequence):
        sequence = [int(x)%len(self.notes.values()) for x in sequence]
        i = 0
        player = True
        while player:
            if i >= len(sequence):
                i = 0
            index = sequence[i]
            list(self.notes.values())[index].play()
            i +=1 
            time.sleep(self.beat)
            player = self.quit_player()

#create a class of multiple note options. 
class NoteChoices:
    def __init__(self, x=None, screen=None):
        self.button_r = 15
        self.screen = screen
        self.x = x
        self.start_color = (255,0,0)
        self.select_color = (0,255,0)
        self.note = None #this is the currently selected note for the column
        self.notes = {} #these are all of the notes sorted as coordinates as key and the value is the note index

    #draw a column of buttons
    def draw_buttons(self, input_location_y, input_height, button_r):
        for i in range(5):
            y = int(input_location_y + input_height*(5-i)/6)
            self.notes[(self.x,y)] = i
            pygame.draw.circle(self.screen, self.start_color, (self.x, y), self.button_r)

    def select_note(self, x, y):
        if self.note:
            pygame.draw.circle(self.screen, self.start_color, self.note, self.button_r)
        self.note = (x,y)
        pygame.draw.circle(self.screen, self.select_color, self.note, self.button_r)

    def get_selected_note(self):
        #returns index i
        return self.notes[self.note]
