import sys, os
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt
#class to create notes
class NoteGenerator:
    def __init__(self):
        self.scales = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}
    
    def generate_note(self, frequency=1):
        n_samples = 44100
        sample_rate = 44100
        N = int(sample_rate/frequency) #change 1 to frequence once bug of frequency is dict is worked out
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

    def write_wave(self, file_name, data):
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
    def __init__(self, beat=1):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.beat = beat
        self.pm_notes = {'C4': 262, 'Eb': 311, 'F': 349, 'G': 391, 'Bb': 466}
        self.scales = {'pm_notes': self.pm_notes}
        self.notes = {}
        self.note_gen = NoteGenerator()


    def add_notes(self, file_name):
        self.notes[file_name] = pygame.mixer.Sound(file_name)

    def quit_player(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
        return True

    #if the notes don't exist, this function will create a new WAV file for the note
    def populate_notes(self):
        for name, frequency in list(self.scales['pm_notes'].items()):
            file_name = name+'.wav'
            if not os.path.exists(file_name):
                data = self.note_gen.generate_note(frequency) #add options to modify the frequency and other params
                self.note_gen.write_wave(file_name, data)
            self.add_notes(os.path.join('scales',file_name))


    def play_sequence(self, sequence): #takes in a sequence of integers and plays the corresponding notes
        self.populate_notes()
        #sequence = [int(x)%len(self.scales['pm_notes'].values()) for x in sequence]
        #want to make a list of file names, self.notes[key=filename, value = wav file]
        #create a list of keys in self.notes
        sequence = [list(self.notes.keys())[x] for x in sequence]
        i = 0
        player = True
        while player:
            if i >= len(sequence):
                i = 0
            #want to call file 'scales/C4' etc.
            index = sequence[i]
            #list(self.notes.values())[index].play()
            self.notes[index].play()
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
