import tkinter as tk
from outer_bar import OuterBar
from tkinter import messagebox
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
        self.outer_bar = OuterBar(self, radius=320)
        self.outer_bar.place(relx=0.5, rely=0.5, anchor='center')
        self.setup_window()

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

        # Add components
        self.text_area = tk.Text(self, wrap='word', font=('Arial', 12), bd=0, padx=10, pady=10)
        self.text_area.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.6, relheight=0.6)

        # Allow dragging the window
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self.x
        y = self.winfo_pointery() - self.y
        self.geometry(f"+{x}+{y}")

    def run(self):
        self.mainloop()