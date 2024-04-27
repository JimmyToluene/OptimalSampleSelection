import sys
from tkinter import messagebox, Entry, Listbox, Frame, Label, Button, Scrollbar, Radiobutton
import tkinter as tk
import os
import random
import GreedyAlgorithm
import time
from threading import Thread
import threading

import easteregg


class SampleSelectionSystem(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.semaphore = threading.Semaphore(value=1)
        self.del_btn = None
        self.exc_btn = None
        self.store_btn = None
        self.GreedyAlgorithm = None
        self.random_combination = None
        self.controller = controller
        self.parameters_info = {
            'm': "45<=m<=54",
            'n': "7<=n<=25",
            'k': "4<=k<=7",
            'j': "s<=j<=k",
            's': "3<=s<=7"
        }
        self.entries = {}
        self.user_input_entries = []
        self.radio_selection = tk.StringVar(value="input")
        self.init_ui()
        #interface.MainApp.progressbar = ttk.Progressbar(self)
        #interface.MainApp.progressbar.place(x=30, y=60, width=200)





    def init_ui(self):
        message_label = Label(self, text="An Optimal Sample Selection System", font=("Arial", 32))
        message_label.pack(pady=(20, 0))

        # Initialize UI elements
        line_frames = [Frame(self) for _ in range(3)]
        for i, frame in enumerate(line_frames):
            frame.pack(fill='x', padx=20, pady=5)

        # Setup input fields
        for i, param in enumerate(['m', 'n']):
            self.entries[param] = self.create_input_field(line_frames[1], param, self.parameters_info[param])
        for param in ['k', 'j', 's']:
            self.entries[param] = self.create_input_field(line_frames[2], param, self.parameters_info[param])

        button_frame = Frame(self)
        button_frame.pack(fill='x', padx=20, pady=10)
        parent_frame = Frame(self)
        parent_frame.pack(fill='x', padx=20, pady=(10, 5))

        self.setup_radio_buttons(button_frame)
        self.setup_action_buttons(button_frame)
        self.user_input_entry(parent_frame)
        self.update_entry_states()
        self.setup_listbox_frame(self)





    def update_ui_start(self):
        self.results_listbox.delete(0, tk.END)
        self.entries['m'].config(state=tk.DISABLED)
        self.entries['n'].config(state=tk.DISABLED)
        self.entries['k'].config(state=tk.DISABLED)
        self.entries['j'].config(state=tk.DISABLED)
        self.entries['s'].config(state=tk.DISABLED)
        for entry in self.user_input_entries:
            entry.config(state=tk.DISABLED)
        self.store_btn.config(state=tk.DISABLED)
        self.exc_btn.config(state=tk.DISABLED)
        self.del_btn.config(state=tk.DISABLED)


    def update_ui_end(self):
        self.entries['m'].config(state=tk.NORMAL)
        self.entries['n'].config(state=tk.NORMAL)
        self.entries['k'].config(state=tk.NORMAL)
        self.entries['j'].config(state=tk.NORMAL)
        self.entries['s'].config(state=tk.NORMAL)
        for entry in self.user_input_entries:
            entry.config(state=tk.NORMAL)
        self.store_btn.config(state=tk.NORMAL)
        self.exc_btn.config(state=tk.NORMAL)
        self.del_btn.config(state=tk.NORMAL)

    def create_input_field(self, parent, parameter_name, additional_info):
        frame = Frame(parent)
        frame.pack(side=tk.LEFT, padx=10, anchor="w")
        label = Label(frame, text=f"{parameter_name}:", font=("Arial", 10))
        label.pack(side=tk.LEFT)
        entry = Entry(frame, width=7)
        entry.pack(side=tk.LEFT, padx=(5, 2))
        additional_text = Label(frame, text=additional_info, font=("Arial", 10))
        additional_text.pack(side=tk.LEFT)
        return entry

    def setup_radio_buttons(self, parent_frame):
        radio_frame = Frame(parent_frame)
        radio_frame.pack(side=tk.LEFT, expand=True, fill='both')
        Radiobutton(radio_frame, text="Random n", variable=self.radio_selection, value="random", font=("Arial", 10),
                    command=self.update_entry_states).pack(side=tk.LEFT, padx=(10, 20))
        Radiobutton(radio_frame, text="Input n", variable=self.radio_selection, value="input", font=("Arial", 10),
                    command=self.update_entry_states).pack(side=tk.LEFT, padx=(0, 20))

    def setup_action_buttons(self, parent_frame):
        action_frame = Frame(parent_frame)
        action_frame.pack(side=tk.LEFT, expand=True, fill='both')
        self.store_btn = Button(action_frame, text="Store DB", font=("Arial", 10), command=self.save_results)
        self.store_btn.pack(side=tk.LEFT,padx=(0, 20))
        self.exc_btn = Button(action_frame, text="Execute", font=("Arial", 10), command=self.Threading)
        self.exc_btn.pack(side=tk.LEFT,padx=(0, 20))
        self.del_btn = Button(action_frame, text="Delete", font=("Arial", 10), command=self.delete_button)
        self.del_btn.pack(side=tk.LEFT, padx=(0, 20))


    def delete_button(self):
        self.value_input_listbox.delete(0,tk.END)
        self.results_listbox.delete(0, tk.END)


    def user_input_entry(self, parent_frame):
        for i in range(1, 26):
            entry = Entry(parent_frame, width=5)
            entry.grid(row=0, column=i, padx=2)
            entry.config(state="disabled")
            self.user_input_entries.append(entry)
            label = Label(parent_frame, text=str(i), font=("Arial", 8))
            label.grid(row=1, column=i)

    def update_entry_states(self):
        state = "normal" if self.radio_selection.get() == "input" else "disabled"
        for entry in self.user_input_entries:
            entry.config(state=state)
        entries_state = "disabled" if self.radio_selection.get() == "input" else "normal"
        self.entries['m'].config(state=entries_state)
        self.entries['n'].config(state=entries_state)

    def setup_listbox_frame(self, root):
        listbox_frame = Frame(root)
        listbox_frame.pack(fill='both', expand=True, padx=20, pady=10)

        value_input_frame = Frame(listbox_frame)
        value_input_frame.pack(side=tk.LEFT, fill='both', expand=True)
        label_value_input = Label(value_input_frame, text="Value Input")
        label_value_input.pack()
        value_input_scrollbar = Scrollbar(value_input_frame)
        value_input_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.value_input_listbox = Listbox(value_input_frame, yscrollcommand=value_input_scrollbar.set,
                                           font=("Arial", 20))
        self.value_input_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        value_input_scrollbar.config(command=self.value_input_listbox.yview)

        results_frame = Frame(listbox_frame)
        results_frame.pack(side=tk.LEFT, fill='both', expand=True, padx=(10, 0))
        label_results = Label(results_frame, text="Results")
        label_results.pack()
        results_scrollbar = Scrollbar(results_frame)
        results_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.results_listbox = Listbox(results_frame, yscrollcommand=results_scrollbar.set, font=("Arial", 20))
        self.results_listbox.pack(side=tk.LEFT, fill='both', expand=True)
        results_scrollbar.config(command=self.results_listbox.yview)

        buttons_frame = Frame(listbox_frame)
        buttons_frame.pack(side=tk.LEFT, padx=(10, 0))
        print_button = Button(buttons_frame, text="Print", font=("Arial", 10),command=self.print_file)
        print_button.pack(pady=(0, 10))
        next_button = Button(buttons_frame, text="Next", font=("Arial", 10),
                             command=lambda: self.controller.show_frame("SecondPage"))
        next_button.pack()

    def Threading(self):
        self.update_ui_start()
        # Acquire the semaphore before creating the thread
        self.semaphore.acquire()
        try:
            # Create and start the thread
            t1 = threading.Thread(target=self.execute_action)
            t1.start()
        finally:
            # Release the semaphore after thread creation
            self.semaphore.release()
    def execute_action(self):
        running_index = 0
        running_index = running_index + 1
        if self.radio_selection.get() == "input":
            self.execute_input(self,running_index)
        elif self.radio_selection.get() == "random":
            self.execute_random(self,running_index)


    @staticmethod
    def execute_input(self,running_index):
        self.value_input_listbox.delete(0, tk.END)
        for i, entry in enumerate(self.user_input_entries, start=1):
            input_value = entry.get()
            if input_value.strip():
                self.value_input_listbox.insert(tk.END, f"{i}st #: {input_value}")
            else:
                continue

        try:
            samples = [int(entry.get()) for entry in self.user_input_entries if entry.get().isdigit()]
            k = int(self.entries['k'].get())
            j = int(self.entries['j'].get())
            s = int(self.entries['s'].get())
            messagebox.showinfo("Executing!", "Please wait for executing!")
            begin = time.time()

            self.chosen_groups = GreedyAlgorithm.Greedy.MainAlgorithm(samples, k, j, s)
            end = time.time()
            messagebox.showinfo("Finished!",f"Total time:{end-begin}")
            self.results_listbox.delete(0, tk.END)
            for i, group in enumerate(self.chosen_groups, start=1):
                self.results_listbox.insert(tk.END, f"{i} ({', '.join(map(str, group))})")
            self.summary_text = f"X-{len(samples)}-{k}-{j}-{s}-{running_index}-{len(self.chosen_groups)}"
            self.results_listbox.insert(tk.END, self.summary_text)
            time.time(2)
            self.update_ui_end()
        except Exception as e:
            print("Error:", str(e))


    @staticmethod
    def execute_random(self,running_index):
        self.value_input_listbox.delete(0, tk.END)
        m = int(self.entries['m'].get())
        n = int(self.entries['n'].get())
        samples = list(range(1, m + 1))  # Generate a list from 1 to m
        random_combination = random.sample(samples, n)
        random_combination.sort()
        index = len(random_combination)
        for index in range(0, index):
            self.value_input_listbox.insert(tk.END, f"{index + 1}st #: {random_combination[index]}")
        k = int(self.entries['k'].get())
        j = int(self.entries['j'].get())
        s = int(self.entries['s'].get())
        messagebox.showinfo("Executing!", "Please wait for executing!")
        begin = time.time()
        self.chosen_groups = GreedyAlgorithm.main_algorithm(random_combination, k, j, s)
        end = time.time()
        messagebox.showinfo("Finished!", f"Total time:{end - begin}")
        self.results_listbox.delete(0, tk.END)
        for i, group in enumerate(self.chosen_groups, start=1):
            self.results_listbox.insert(tk.END, f"{i}              ({', '.join(map(str, group))})")
        self.summary_text = f"{m}-{n}-{k}-{j}-{s}-{running_index}-{len(self.chosen_groups)}"
        self.results_listbox.insert(tk.END, self.summary_text)
        self.update_ui_end()
        sys.exit()


#    def execute_ction(self):
#        running_index = 0
#        running_index = running_index + 1
#        if self.radio_selection.get() == "input":
#            self.value_input_listbox.delete(0, tk.END)
#            for i, entry in enumerate(self.user_input_entries, start=1):
#                input_value = entry.get()
#                if input_value.strip():
#                    self.value_input_listbox.insert(tk.END, f"{i}st #: {input_value}")
#                else:
#                    continue
#
#           try:
#               samples = [int(entry.get()) for entry in self.user_input_entries if entry.get().isdigit()]
#                k = int(self.entries['k'].get())
#               j = int(self.entries['j'].get())
#                s = int(self.entries['s'].get())
#                messagebox.showinfo("Executing!", "Please wait for executing!")
#                self.chosen_groups = GreedyAlgorithm.Greedy.MainAlgorithm(samples, k, j, s)
#                messagebox.showinfo("Finished!")
#                self.results_listbox.delete(0, tk.END)
#                for i, group in enumerate(self.chosen_groups, start=1):
#                    self.results_listbox.insert(tk.END, f"{i} ({', '.join(map(str, group))})")
#                self.summary_text = f"X-{len(samples)}-{k}-{j}-{s}-{running_index}-{len(self.chosen_groups)}"
#                self.results_listbox.insert(tk.END, self.summary_text)
#            except Exception as e:
#                print("Error:", str(e))
#
#        elif self.radio_selection.get() == "random":
#            self.value_input_listbox.delete(0, tk.END)
#            m = int(self.entries['m'].get())
#            n = int(self.entries['n'].get())
#            samples = list(range(1, m + 1))  # Generate a list from 1 to m
#            self.random_combination = random.sample(samples, n)
#            self.random_combination.sort()
#
#            index = len(self.random_combination)
#            for index in range(0, index):
#                self.value_input_listbox.insert(tk.END, f"{index + 1}st #: {self.random_combination[index]}")
#            k = int(self.entries['k'].get())
#            j = int(self.entries['j'].get())
#            s = int(self.entries['s'].get())
#
#            messagebox.showinfo("Executing!", "Please wait for executing!")
#            self.chosen_groups = GreedyAlgorithm.Greedy.MainAlgorithm(self.random_combination,k,j,s)
#            messagebox.showinfo("Finished!")
#            self.results_listbox.delete(0, tk.END)
#            for i, group in enumerate(self.chosen_groups, start=1):
#                self.results_listbox.insert(tk.END, f"{i}              ({', '.join(map(str, group))})")
#            self.summary_text = f"{m}-{n}-{k}-{j}-{s}-{running_index}-{len(self.chosen_groups)}"
#           self.results_listbox.insert(tk.END, self.summary_text)
#
    def save_results(self):
        """Save the results to a file in a directory named 'database'."""
        if not self.chosen_groups or not self.summary_text:
            messagebox.showerror("Error", "No results to save, please perform the operation first.")
            return

        # Ensure the 'database' directory exists
        directory = "database"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Construct the file path
        file_path = os.path.join(directory, f"{self.summary_text}.txt")

        try:
            with open(file_path, "w") as file:
                file.write(f"({', '.join(map(str, self.random_combination))})\n")
                for line in self.chosen_groups:
                    file.write(f"({', '.join(map(str, line))})\n")
                file.write(self.summary_text)
            messagebox.showinfo("Success", f"Results successfully saved to file: {file_path}")
            os.startfile(f"{self.summary_text}.txt", "print")
        except IOError as e:
            messagebox.showerror("Failure", f"Error saving file: {str(e)}")

    def print_file(self):
        if not self.chosen_groups or not self.summary_text:
            messagebox.showerror("Error", "No results to save, please perform the operation first.")
            return

        # Ensure the 'database' directory exists
        directory = "database"
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Construct the file path
        file_path = os.path.join(directory, f"{self.summary_text}.txt")

        try:
            with open(file_path, "w") as file:
                file.write(f"({', '.join(map(str, self.random_combination))})\n")
                for line in self.chosen_groups:
                    file.write(f"({', '.join(map(str, line))})\n")
                file.write(self.summary_text)
            os.startfile(f"{self.summary_text}.txt", "print")
        except IOError as e:
            pass

        # Implement functionality to print the selected file


