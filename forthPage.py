import tkinter as tk
from tkinter import Label, Frame


class Page4(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        label = Label(self, text="This is the 4th page", font=("Arial", 24))
        label.pack(pady=100)

        back_button = tk.Button(self, text="Go Back to Second Page",
                                command=lambda: controller.show_frame("ThirdPage"))
        back_button.pack()