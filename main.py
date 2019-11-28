import sys, os
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

pm_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}

#eventually have a dict of different scales to reactivley draw on display
scales_dict = {}
scales_dict['pm_notes'] = pm_notes


def generate_note(frequency):
    n_samples = 44100
    sample_rate = 44100
    N = int(sample_rate/frequency)
    #generting a ring bugger
    buffer = deque([random.random() - .5 for i in range(N)])
    #initialize a samples buffer
    samples = np.array([0]*n_samples, 'float32')
    for i in range(n_samples):
        samples[i] = buffer[0]
        average = .996*.5*(buffer[0]+buffer[1])
        buffer.append(average)
        buffer.popleft()

    #convert samples to 16 bit values then to string
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

def write_wave(file_name, data):
    if os.path.isdir(os.path.join('scales')) == False:
        os.mkdir('scales')
    file = wave.open(os.path.join('scales',file_name), 'wb')
    #WAV file parameters
    n_channels = 1
    sample_width = 2
    frame_rate = 44100
    n_frames = 44100
    #setting WAV parameters
    file.setparams((n_channels, sample_width, frame_rate, n_frames,'NONE', 'noncompressed'))
    file.writeframes(data)
    file.close


#class for playing a WAV file
class NotePlayer:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.notes = {} #dictionary of all possible notes

    def add_notes(self, file_name):
        self.notes[file_name] = pygame.mixer.Sound(file_name)

    def quit_player(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
        return True

    def play_sequence(self, sequence, beat=1):
        sequence = [int(x)%len(self.notes.values()) for x in sequence]
        i = 0
        player = True
        while player:
            player = self.quit_player()
            if i >= len(sequence):
                i = 0
            index = sequence[i]
            list(self.notes.values())[index].play()
            i +=1 
            time.sleep(beat)

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


class Display(NoteChoices, NotePlayer):
    pygame.init()
    def __init__(self):
        self.width = 1000
        self.height = 500
        self.background = (255, 255, 255)
        self.screen = None
        self.note_buttons_positions = [] #keeps a list of all button positions for reference
        self.notes = [] #gets added with value of note button pressed (between 1 and 5)
        self.sequence = [0]*5
        self.note_player = NotePlayer()
        self.button_r = NoteChoices().button_r
        self.scale = 'pm_notes'

    NoteChoices().__init__()
    button_r = NoteChoices().button_r
    
    #will allow users to change the music scale
    def delect_scale(self, scale='pm_notes'):
        self.scale = scale

    #if the notes don't exist, this function will create a new WAV file for the note
    def populate_notes(self):
        for name, frequency in list(scales_dict[self.scale].items()):
            file_name = name+'.wav'
            if not os.path.exists(file_name):
                data = generate_note(frequency) #add options to modify the frequency and other params
                write_wave(file_name, data)
            self.note_player.add_notes(os.path.join('scales',file_name))

    #draws a circular button that the user can click on
    def note_button_generator(self, x, y, color=(255,0,0)):
        pygame.draw.circle(self.screen, color, (x, y), (button_r))

    #this creates the box that the note selections are drawn in
    def input_box(self):
        input_location_x = int(self.width/4)
        input_location_y = 20
        input_width = int(self.width/2)
        input_height = int(self.height/2)
        input_box = pygame.Rect(input_location_x, input_location_y, input_width, input_height)
        pygame.draw.rect(self.screen, (100,100,100), input_box)
        #pull the below functionality into its own function
        for i in range(5):
            pygame.draw.line(self.screen, (0,0,0), (input_location_x, input_location_y+int(input_height*(1+i)/6)), (input_location_x+input_width, input_location_y+int(input_height*(1+i)/6)))
        for i in range(5):
            x = int(input_location_x + input_width*(i+1)/6)
            notes = NoteChoices(x, self.screen)
            self.notes.append(notes)
            notes.draw_buttons(input_location_y, input_height, self.button_r)

    #detects if the user clicked on the screen. if they have, add note to list and change color of note
    def detect_select(self, x, y):
        for i in range(len(self.notes)):
            for pos in self.notes[i].notes.keys():
                if x in range(pos[0]-self.button_r, pos[0]+self.button_r):
                    if y in range(pos[1]-self.button_r, pos[1]+self.button_r):
                        self.notes[i].select_note(pos[0], pos[1])
                        note = self.notes[i].get_selected_note()
                        self.sequence[i] = note

    #plays the sequence of notes that the user has input into the program
    def play_sequence(self):
        self.note_player.play_sequence(self.sequence)

    #this sets theparamaters for the instruction text
    def display_directions(self):
        pygame.font.init()
        my_font = pygame.font.SysFont('Comic Sans MS', 40)
        instruct = my_font.render('Select circles to choose note at that beat', False, (0,0,0))
        play = my_font.render('Press \'p\' to play tone', False, (0,0,0))
        quit = my_font.render('Press \'q\' to stop playing tone', False, (0,0,0)) 
        self.screen.blit(instruct, (self.width//2-instruct.get_width()//2, 40+self.height//2))
        self.screen.blit(play, (self.width//2-play.get_width()//2, -30+self.height*3//4))
        self.screen.blit(quit, (self.width//2-quit.get_width()//2, self.height*3//4))

    #this draws the main screen window. this needs to be called for the program to initiaize
    def display_screen(self):
        self.populate_notes()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Josh\'s Music Maker')
        self.screen.fill(self.background)
        self.input_box()
        self.display_directions()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_location = pygame.mouse.get_pos()
                    self.detect_select(mouse_location[0], mouse_location[1])
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.play_sequence()
            pygame.display.update()


def main():
    Display().display_screen()

if __name__ == '__main__':
    main()
