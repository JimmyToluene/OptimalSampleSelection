
import tkinter as tk
from tkinter import Label, Radiobutton, Button, Frame, StringVar

import forthPage


class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        back_button = tk.Button(self, text="Go Back to Second Page",
                                command=lambda: controller.show_frame("SecondPage"))
        message_label = Label(self, text="An Optimal Sample Selection System", font=("Arial", 32))
        message_label.pack(pady=(20, 0))
        self.filter_var = tk.StringVar(value="None")  # Default no selection

        # Label for instructions
        label = Label(self, text="Please select the filter method:", font=("Arial", 27))
        label.pack(pady=20)

        filters = ["Define positions and numbers", "Define positions and range of numbers", "Select positions as fixed numbers"]
        for method in filters:
            Radiobutton(self, text=method, font=("Arial", 20),variable=self.filter_var, value=method).pack()

        # Button to go to the next appropriate page
        next_button = Button(self, text="Next", command=self.go_next,)
        next_button.pack(side=tk.RIGHT,padx=(0,200))
        back_button = tk.Button(self, text="Previous",
                                command=lambda: controller.show_frame("SecondPage"))
        back_button.pack(side=tk.RIGHT,padx=20)

    def go_next(self):
        selected_filter = self.filter_var.get()
        if selected_filter == "Define positions and numbers":
            self.controller.show_frame("Page4")
            forthPage.Page4.value_input_listbox.delete(0, tk.END)
        elif selected_filter == "Define positions and range of numbers":
            self.controller.show_frame("Page5")
        elif selected_filter == "Select positions as fixed numbers":
            self.controller.show_frame("Page6")
        else:
            tk.messagebox.showerror("Selection Error", "Please select a filter method before proceeding.")