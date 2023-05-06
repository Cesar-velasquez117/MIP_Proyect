import customtkinter as ctk
class SlidePanel(ctk.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master=parent)

        #general attributes
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = abs(start_pos-end_pos)

        #animation logic
        self.pos = self.end_pos
        self.in_end_pos = True

        #layout
        self.place(relx = self.end_pos, rely = 0.1, relwidth = self.width, relheight = 0.8)

    def animate(self):
        if self.in_end_pos:
            self.animate_forward()
        else:
            self.animate_backwards()
    
    def animate_forward(self):
        if self.pos < self.start_pos:
            self.pos +=0.008
            self.place(relx = self.pos, rely = 0.1, relwidth = self.width, relheight = 0.8)
            self.after(10, self.animate_forward)
        else:
            self.in_end_pos = False

    def animate_backwards(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx = self.pos, rely = 0.1, relwidth = self.width, relheight = 0.8)
            self.after(10, self.animate_backwards)
        else:
            self.in_end_pos = True