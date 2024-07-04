import tkinter as tk

import win32gui
from PIL import Image, ImageTk, ImageDraw

class RadialText(tk.Canvas):
    def __init__(self, master, radius, **kwargs):
        super().__init__(master, width=2*radius, height=2*radius, bg='white', highlightthickness=0, **kwargs)
        self.master = master
        self.radius = radius
        self.create_oval(0, 0, 2*radius, 2*radius, outline='black', width=2)
        self.create_circle_mask()
        self.create_text_area()

    def create_text_area(self):
        self.text_area = tk.Text(self, wrap='word', font=('Arial', 12), bd=0, padx=10, pady=10, width=30, height=10, bg='white', fg='black')
        self.text_area.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=1, relheight=1)

    def create_circle_mask(self):
        size = 2 * self.radius
        mask = Image.new('L', (size, size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, size, size), fill=255)
        mask = ImageTk.PhotoImage(mask)

        # Apply the mask to the window
        hwnd = self.winfo_id()  # Get the correct window handle
        bounds = (0, 0, size, size)
        hrgn = win32gui.CreateEllipticRgnIndirect(bounds)
        win32gui.SetWindowRgn(hwnd, hrgn, True)

    def get_text_content(self):
        return self.text_area.get("1.0", tk.END)

    def set_text_content(self, content):
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, content)