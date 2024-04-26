import tkinter as tk
from tkinter import messagebox, Entry, Listbox, Frame, Label, Button, Scrollbar, Radiobutton
import os
import interface

class Page6(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.entries = {}
        self.filter_var = tk.StringVar(value="None")  # Default no selection
        self.init_ui()
        self.setup_listbox_frame(self)
        back_button = tk.Button(self, text="Go Back to Second Page",
                                command=lambda: controller.show_frame("ThirdPage"))

    def init_ui(self):
        message_label = Label(self, text="An Optimal Sample Selection System", font=("Arial", 32))
        message_label.pack(pady=(20, 0))
        label = Label(self, text="Select position as fixed numbers", font=("Arial", 27))
        label.pack(pady=20)
        line_frames = Frame(self)
        line_frames.pack(fill='x', padx=200, pady=5)
        pos1_frames = Frame(self)
        pos1_frames.pack(fill='x', padx=200, pady=5)
        Label(pos1_frames, text="Please input 3 positions:", font=(20)).pack(side=tk.LEFT)
        self.entries[1] = self.create_entry_field(pos1_frames, "1st Position")
        self.entries[2] = self.create_entry_field(pos1_frames, "2nd Position")
        self.entries[3] = self.create_entry_field(pos1_frames, "3nd Position")


        pos2_frames = Frame(self)
        pos2_frames.pack(fill='x', padx=200, pady=5)
        Label(pos2_frames,
                    text="Please input the sum of three number in positions",
                    font=(20)).pack(side=tk.LEFT)
        self.entries[4] = self.create_input_field(pos2_frames)

        #self.entries[7] = self.create_entry_field(pos2_frames, "1st Position")
        #self.entries[8] = self.create_entry_field(pos2_frames, "2nd Position")
        #self.entries[9] = self.create_entry_field(pos2_frames, "3rd Position")
        pos3_frame = Frame(self)
        pos3_frame.pack(fill='x', padx=200, pady=5)
        self.entries[5] = self.create_entry_field(pos3_frame, "Please name a file to create")

    def create_input_field(self, parent):
        frame = Frame(parent)
        frame.pack(side=tk.LEFT, anchor="w")
        entry = Entry(frame, width=5)
        entry.pack(side=tk.LEFT, padx=(0, 3))
        return entry

    def create_entry_field(self, parent, parameter_name):
        frame = Frame(parent)
        frame.pack(side=tk.LEFT, padx=10, anchor="w")
        label = Label(frame, text=f"{parameter_name}:", font=("Arial", 10))
        label.pack(side=tk.LEFT)
        entry = Entry(frame, width=5)
        entry.pack(side=tk.LEFT, padx=(1,0))
        return entry


    def setup_listbox_frame(self, parent_frame):
        listbox_frame = Frame(parent_frame)
        listbox_frame.place(x=550, y=450, anchor="center")

        value_input_frame = Frame(listbox_frame)
        value_input_frame.pack(side=tk.LEFT, fill='both', expand=True)

        value_input_scrollbar = Scrollbar(value_input_frame)
        value_input_scrollbar.pack(side=tk.RIGHT, fill='y')

        self.value_input_listbox = Listbox(value_input_frame, yscrollcommand=value_input_scrollbar.set,
                                           font=("Arial", 20), height=8, width=50)
        self.value_input_listbox.pack(side=tk.BOTTOM, fill='both', expand=True)
        value_input_scrollbar.config(command=self.value_input_listbox.yview)

        # Adding buttons for preview, refilter, and print operations
        operation_frame = Frame(listbox_frame)
        operation_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        Button(operation_frame, text="Previous",
               command=lambda: self.controller.show_frame("ThirdPage")).pack(pady=10)
        Button(operation_frame, text="Execute", ).pack(pady=10)
        Button(operation_frame, text="Display",command=self.display_file_content).pack(pady=10)
        Button(operation_frame, text="Print").pack(pady=10)

    def display_file_content(self):
        selected_file = interface.MainApp.selected_file
        if not selected_file:
            messagebox.showwarning("Warning", "No file selected")
            return

        file_path = os.path.join('database', selected_file)
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                # Assuming content needs to be processed similarly to the provided execute_action method
                self.process_file_content(content)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    def process_file_content(self, content):
        self.value_input_listbox.delete(0, tk.END)
        # Simulate processing; real implementation depends on file format and desired processing
        entries = content.split('\n')
        self.value_input_listbox.insert(tk.END, f"Input n number array is {entries[0]}")
        for i, entry in enumerate(entries[1:], start=1):
            if entry == entries[-1]:
                self.value_input_listbox.insert(tk.END, f"{entries[-1]}")
                break
            if entry.strip():
                self.value_input_listbox.insert(tk.END, f"{i}        {entry}")

