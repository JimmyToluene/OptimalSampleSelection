from tkinter import messagebox, Entry, Listbox, Frame, Label, Button, Scrollbar, Radiobutton
import tkinter as tk
import os
import interface

class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.radio_buttons = {}
        self.file_var = tk.StringVar(value='No file selected')
        self.columns = []  # List of column frames
        self.current_column = None  # Current active column frame
        self.controller = controller
        self.init_ui()
        self.setup_action_buttons(self)
        self.setup_filelist_widget()
        self.refresh_file_list()
        self.setup_listbox_frame(self)

    def init_ui(self):
        message_label = Label(self, text="An Optimal Sample Selection System", font=("Arial", 32))
        message_label.pack(pady=(20, 0))

    def display_file_content(self):
        selected_file = self.file_var.get()
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

    def setup_action_buttons(self, parent_frame):
        action_frame = Frame(parent_frame)
        action_frame.pack(pady=10, anchor="center")
        message_label = Label(action_frame, text="Data Base Resources", font=("Arial", 20)).pack(side=tk.LEFT)
        Button(action_frame, text="Display", command=self.display_file_content).pack(side=tk.LEFT, padx=(100, 20))
        Button(action_frame, text="Delete", command=self.delete_selected_file).pack(side=tk.LEFT, padx=(0, 20))

    def load_files_from_directory(self, directory):
        """Load files from the given directory."""
        try:
            # List all files in the directory
            file_list = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
            return file_list
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files from directory: {str(e)}")
            return []

    def setup_filelist_widget(self):
        self.file_frame = Frame(self)
        self.file_frame.place(x=350, y=230, anchor="center")
        self.add_new_column()

    def add_new_column(self):
        new_column = Frame(self.file_frame)
        new_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=70)
        self.columns.append(new_column)
        self.current_column = new_column
        self.radio_buttons_in_current_column = 0

    def refresh_file_list(self):
        directory = 'database'
        try:
            current_files = set(os.listdir(directory))
            existing_files = set(self.radio_buttons.keys())

            added_files = current_files - existing_files
            removed_files = existing_files - current_files

            for file_name in added_files:
                if self.radio_buttons_in_current_column >= 7:
                    self.add_new_column()
                rb = Radiobutton(self.current_column, text=file_name, variable=self.file_var, value=file_name,
                                 anchor="w")
                rb.pack(fill='x')
                self.radio_buttons[file_name] = rb
                self.radio_buttons_in_current_column += 1

            for file_name in removed_files:
                rb = self.radio_buttons.pop(file_name)
                rb.destroy()
                self.radio_buttons_in_current_column -= 1

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load files from directory: {str(e)}")

        # Schedule next refresh
        self.after(5000, self.refresh_file_list)  # Refresh every 5 seconds

    def setup_listbox_frame(self, parent_frame):
        listbox_frame = Frame(parent_frame)
        listbox_frame.pack(side=tk.LEFT,padx=(300,100),pady=(170,0))

        value_input_frame = Frame(listbox_frame)
        value_input_frame.pack(side=tk.LEFT, fill='both', expand=True)

        value_input_scrollbar = Scrollbar(value_input_frame)
        value_input_scrollbar.pack(side=tk.RIGHT, fill='y')

        self.value_input_listbox = Listbox(value_input_frame, yscrollcommand=value_input_scrollbar.set,
                                           font=("Arial", 20), height=10, width=60)
        self.value_input_listbox.pack(side=tk.BOTTOM, fill='both', expand=True)
        value_input_scrollbar.config(command=self.value_input_listbox.yview)

        # Adding buttons for preview, refilter, and print operations
        operation_frame = Frame(listbox_frame)
        operation_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)
        Button(operation_frame, text="Previous",
               command=lambda: self.controller.show_frame("SampleSelectionSystem")).pack(pady=10)
        Button(operation_frame, text="Refilter", command=lambda: self.refilter_files()).pack(pady=10)
        Button(operation_frame, text="Print", command=self.print_file).pack(pady=10)

    def delete_selected_file(self):
        selected_file = self.file_var.get()
        if not selected_file or selected_file == "No file selected":
            messagebox.showwarning("Warning", "No file selected")
            return

        file_path = os.path.join('database', selected_file)
        try:
            os.remove(file_path)
            rb = self.radio_buttons.pop(selected_file)
            rb.destroy()
            self.file_var.set("No file selected")  # Reset the selection
            messagebox.showinfo("Success", "File deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {str(e)}")

    def refilter_files(self):
        selected_file = self.file_var.get()
        if not selected_file or selected_file == "No file selected":
            messagebox.showwarning("Warning", "No file selected")
            return
        interface.MainApp.selected_file = selected_file
        self.controller.show_frame("ThirdPage")
        # Implement functionality to refilter file list based on some criteria
        pass

    def print_file(self):
        # Implement functionality to print the selected file
        filename = "database/" + self.file_var.get()
        selected_file = Path(filename).absolute()
        print(selected_file)
        if selected_file:
            messagebox.showinfo("Print", f"Printing {selected_file}")
            win32api.ShellExecute(0, 'print', selected_file, f'/d:"{win32print.GetDefaultPrinter()}"', '.', 0)
        else:
            messagebox.showwarning("Warning", "No file selected")
