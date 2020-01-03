import sys
import tkinter as tk
from note_functions import NotePlayer, NoteGenerator

class Display:
    #initial paramaters for display screen
    def __init__(self, num_buttons = 6):
        self.width = 1500
        self.height = 750
        self.window1 = tk.Tk()
        self.lines = []
        self.button_locations = []
        self.buttons = [] #stores buttons after they're created in the program
        self.num_buttons = num_buttons
        self.notes = [0]*num_buttons #records what notes have been selected. Defaults to 00000
        self.sequences = []

    def screen_settings(self):
        self.window1.title('make your own kind of music') #title of project
        self.window1.geometry(str(self.width)+"x"+str(self.height)) #sets the size of the window
        self.window1.configure(background="white")
        self.window1.resizable(0,0) #disallows user to resize window

    def play_sequence(self):
        for sequence in self.sequences:
            NotePlayer().play_sequence(sequence)

    def add_sequence(self):
        i = len(self.sequences)
        self.sscreen.insert(i, 'sequence '+str(i))
        self.sequences.append(self.notes)

    def clear_sequences(self):
        self.sequences = []

    def remove_sequence(self):
        i = self.sscreen.curselection()[0]
        print(i)
        del self.sequences[int(i)]
        self.sscreen.delete(i)

    #this is the main screen where users can add/ change notes
    def music_note_screen(self):
        self.mnw_width = self.width//2
        self.mnw_height = self.height//2
        self.mnw = tk.Canvas(self.window1, height=self.mnw_height, width = self.mnw_width, bg="black") #mnw stands for music note window
        self.mnw.place(x=self.width//4, y=10)

    #this screen is on the left of the window, which shows the sequences the user has added
    def sequence_screen(self):
        self.sscreen_width = self.width//4
        self.sscreen_height = self.height//2
        self.sscreen = tk.Listbox(self.window1, height=10)
        self.sscreen.place(x=10, y=10)


    def control_buttons(self):
        add_button = tk.Button(self.window1, text= 'add current sequence', command=self.add_sequence)
        play_button = tk.Button(self.window1, text= 'play sequences', command=self.play_sequence)
        delete_button = tk.Button(self.window1, text= 'remove sequence', command=self.remove_sequence)
        clear_button =tk.Button(self.window1, text= 'remove all sequences', command=self.clear_sequences)
        add_button.place(x=self.width//5, y= self.height*2//3)
        play_button.place(x=2*self.width//5, y= self.height*2//3)
        delete_button.place(x=3*self.width//5, y= self.height*2//3)
        clear_button.place(x=4*self.width//5, y= self.height*2//3)

    def update_notes(self, line, note): #updates the notes array with the currently selected note
        self.notes[line] = abs(self.num_buttons-note) 
        print(self.notes)

    def refresh_buttons(self, i):
        for button in self.buttons:
            if button[1] == i:
                self.mnw.itemconfig(button[0], fill='red')

    def combine_button(self, line, note, button): #update notes is in this function, all three events happen when note is clicked
        self.update_notes(line, note)
        self.refresh_buttons(line)
        self.mnw.itemconfig(button, fill='green')

    def draw_button(self, x1, y1, x2, y2, r, line, note): #draws each button
        x = x1+r
        y = y1+r
        new_button = self.mnw.create_oval(x1, y1, x2, y2, fill='red')
        self.buttons.append([new_button, line, note]) #keeps buttons in relation to line and buttons and notes
        self.mnw.tag_bind(new_button, '<Button-1>', lambda event: self.combine_button(line, note, new_button))
            
    def draw_mnw_lines(self):
        r = 10
        for x in range(6): #creates (x0,y0) and (x1,y1) positions for each vertical line of notes
            x_position = int(((x+1)/7)*self.mnw_width)
            self.lines.append([x_position,0, x_position, self.mnw_height]) #in format x1, y1, x2, y2
        for line in self.lines: #draws each line and fills in with red color
            self.mnw.create_line(line[0], line[1], line[2], line[3], fill="red")
            x = line[0]
            for b in range(self.num_buttons): #creates each button location
                h = self.mnw_height*(b+1)//(self.num_buttons+1)
                self.button_locations.append([x-r, h-r, x+r, h+r, self.lines.index(line), b])
        for b in self.button_locations:
            self.draw_button(b[0], b[1], b[2], b[3], r, b[4], b[5])


    def display_screen(self):
        self.screen_settings()
        self.control_buttons()
        self.music_note_screen()
        self.sequence_screen()
        self.draw_mnw_lines()
        self.window1.mainloop()


#NotePlayer().populate_notes()
Display().display_screen()

        
