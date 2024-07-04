import subprocess
import tkinter as tk
from outer_bar import OuterBar
from radial_text import RadialText
from tkinter import messagebox, filedialog
from PIL import Image, ImageDraw, ImageTk
import win32gui
import win32con


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Radial Notepad')
        self.geometry('700x700')
        self.resizable(False, False)
        self.overrideredirect(True)
        self.setup_window()
        self.outer_bar = OuterBar(self, radius=350)
        self.outer_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.radial_text = RadialText(self, radius=310)
        self.radial_text.place(relx=0.5, rely=0.5, anchor='center')

    def setup_window(self):
        # Create a circular mask
        size = 700
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        mask = ImageTk.PhotoImage(mask)

        # Apply the mask to the window
        hwnd = self.winfo_id()  # Get the correct window handle
        bounds = (0, 0, size, size)
        hrgn = win32gui.CreateEllipticRgnIndirect(bounds)
        win32gui.SetWindowRgn(hwnd, hrgn, True)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    text_content = self.radial_text.get_text_content()
                    file.write(text_content)
                messagebox.showinfo("Success", "File saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while saving the file: {e}")

    def save_file_as(self):
        self.save_file()

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    text_content = file.read()
                    self.radial_text.set_text_content(text_content)
                messagebox.showinfo("Success", "File opened successfully")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while opening the file: {e}")

    def new_window(self):
        subprocess.Popen(["python", "main.py"])

    def run(self):
        self.mainloop()

    def apply_light_theme(self):
        self.configure(bg="white")
        self.radial_text.text_area.configure(bg="white", fg="black", insertbackground="black")

    def apply_dark_theme(self):
        self.configure(bg="black")
        self.radial_text.text_area.configure(bg="black", fg="white", insertbackground="cyan")

    def copy_text(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.radial_text.text_area.selection_get())
        except tk.TclError:
            messagebox.showerror("Error", "Nothing selected to copy")

    def paste_text(self):
        try:
            self.radial_text.text_area.insert(tk.INSERT, self.clipboard_get())
        except tk.TclError:
            messagebox.showerror("Error", "Nothing to paste from clipboard")

    def delete_text(self):
        try:
            self.radial_text.text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
        except tk.TclError:
            messagebox.showerror("Error", "Nothing selected to delete")

    def select_all_text(self):
        self.radial_text.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.radial_text.text_area.mark_set(tk.INSERT, "1.0")
        self.radial_text.text_area.see(tk.INSERT)

