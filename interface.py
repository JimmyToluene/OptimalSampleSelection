import tkinter as tk
from tkinter import messagebox, Entry, Listbox, Frame, Label, Button, Scrollbar, Radiobutton
import FirstFrame
import SecondPage
import easteregg
import fifthPage
import forthPage
import sixthPage
import thirdPage

class MainApp(tk.Tk):
    selected_file = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sample Selection System")
        self.geometry("1920x1080")
        # Container setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (FirstFrame.SampleSelectionSystem, SecondPage.SecondPage,thirdPage.ThirdPage,forthPage.Page4,fifthPage.Page5,sixthPage.Page6,easteregg.Page7):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SampleSelectionSystem")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
