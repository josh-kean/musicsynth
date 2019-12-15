import sys
import tkinter as tk

class Display:
    #initial paramaters for display screen
    def __init__(self, num_buttons = 6):
        self.width = 1500
        self.height = 750
        self.window1 = tk.Tk()
        self.lines = []
        self.buttons = []
        self.num_buttons = num_buttons
        self.notes = [0]*num_buttons
        self.sequences = []

    def screen_settings(self):
        self.window1.title('make your own kind of music') #title of project
        self.window1.geometry(str(self.width)+"x"+str(self.height)) #sets the size of the window
        self.window1.configure(background="white")
        self.window1.resizable(0,0) #disallows user to resize window

    def play_sequence(self):
        print('functionality to be added')

    def add_sequence(self):
        self.sequences.append(self.notes)

    def clear_sequences(self):
        self.sequences = []

    def remove_sequence(self):
        print('functionality to be added')

    def music_note_screen(self):
        self.mnw_width = self.width//2
        self.mnw_height = self.height//2
        self.mnw = tk.Canvas(self.window1, height=self.mnw_height, width = self.mnw_width, bg="black") #mnw stands for music note window
        self.mnw.place(x=self.width//4, y=10)

    def sequence_screen(self):
        self.

    def control_buttons(self):
        add_button = tk.Button(self.window1, text= 'add current sequence', command=self.add_sequence)
        play_button = tk.Button(self.window1, text= 'play sequences', command=self.play_sequence)
        delete_button = tk.Button(self.window1, text= 'remove sequence', command=self.remove_sequence)
        clear_button =tk.Button(self.window1, text= 'remove all sequences', command=self.clear_sequences)
        add_button.place(x=self.width//5, y= self.height*2//3)
        play_button.place(x=2*self.width//5, y= self.height*2//3)
        delete_button.place(x=3*self.width//5, y= self.height*2//3)
        clear_button.place(x=4*self.width//5, y= self.height*2//3)

    def update_notes(self, line, note):
        self.notes[line] = abs(self.num_buttons-note)
        print(line, note)

    def draw_button(self, x1, y1, x2, y2, r, line, note):
        x = x1+r
        y = y1+r
        new_button = self.mnw.create_oval(x1, y1, x2, y2, fill='red')
        self.mnw.tag_bind(new_button, '<Button-1>', lambda event: self.update_notes(line, note))
            
    def draw_mnw_lines(self):
        r = 10
        for x in range(6):
            x_position = int(((x+1)/7)*self.mnw_width)
            self.lines.append([x_position,0, x_position, self.mnw_height]) #in format x1, y1, x2, y2
        for line in self.lines:
            self.mnw.create_line(line[0], line[1], line[2], line[3], fill="red")
            x = line[0]
            for b in range(self.num_buttons):
                h = self.mnw_height*(b+1)//(self.num_buttons+1)
                self.buttons.append([x-r, h-r, x+r, h+r, self.lines.index(line), b])
        for b in self.buttons:
            self.draw_button(b[0], b[1], b[2], b[3], r, b[4], b[5])


    def display_screen(self):
        self.screen_settings()
        self.control_buttons()
        self.music_note_screen()
        self.draw_mnw_lines()
        self.window1.mainloop()


Display().display_screen()

        
