import tkinter as tk
from math import radians, cos, sin
import win32gui
from tkinter import font
from PIL import ImageDraw, ImageTk, Image

class OuterBar(tk.Canvas):
    def __init__(self, master, radius, **kwargs):
        super().__init__(master, width=2*radius, height=2*radius, bg='darkgrey', **kwargs)
        self.main_window = master
        self.radius = radius
        self.create_oval(0, 0, 2*radius, 2*radius, outline='black', width=2)
        self.create_circle_mask()

        # Allow dragging the window
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)

        self.create_separator(45, 329)
        self.create_separator(75, 329)
        self.create_separator(90, 329)
        self.add_buttons()

        self.file_menu = None
        self.edit_menu = None
        self.theme_menu = None



    def create_separator(self, theta, radius):
        canvas_center = self.radius  # 350, the center of the canvas

        # Calculate left separator
        x1_left = canvas_center + (radius - 20) * cos(radians(theta - 10))
        y1_left = canvas_center - (radius - 20) * sin(radians(theta - 10))
        x2_left = canvas_center + (radius + 20) * cos(radians(theta - 10))
        y2_left = canvas_center - (radius + 20) * sin(radians(theta - 10))

        # Calculate right separator
        x1_right = canvas_center + (radius - 20) * cos(radians(theta + 5))
        y1_right = canvas_center - (radius - 20) * sin(radians(theta + 5))
        x2_right = canvas_center + (radius + 20) * cos(radians(theta + 5))
        y2_right = canvas_center - (radius + 20) * sin(radians(theta + 5))

        print("Creating separator lines: ")
        print(f"Left separator: ({x1_left}, {y1_left}) to ({x2_left}, {y2_left})")
        print(f"Right separator: ({x1_right}, {y1_right}) to ({x2_right}, {y2_right})")

        self.create_line(x1_left, y1_left, x2_left, y2_left, fill="black", width=4)
        self.create_line(x1_right, y1_right, x2_right, y2_right, fill="black", width=4)

    def close_window(self):
        self.main_window.destroy()

    def start_drag(self, event):
        self.main_window.x = event.x
        self.main_window.y = event.y

    def do_drag(self, event):
        x = self.main_window.winfo_pointerx() - self.main_window.x
        y = self.main_window.winfo_pointery() - self.main_window.y
        self.main_window.geometry(f"+{x}+{y}")

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


    def add_buttons(self):
        buttons = [
            ("File", self.open_file_menu),
            ("Edit", self.open_edit_menu),
            ("Theme", self.open_theme_menu),
            ("X", self.close_window)
        ]

        angle_step = -60 / len(buttons)
        start_angle = 88


        for i, (text, command) in enumerate(buttons):
            angle = start_angle + i * angle_step
            x = self.radius + (self.radius - 20) * cos(radians(angle))
            y = self.radius - (self.radius - 20) * sin(radians(angle))
            if text is "X":
                btn = tk.Button(self, text=text, command=command, width=5, bd=0, highlightthickness=0, bg="darkgrey", fg="firebrick", font=("Terminal", 12, 'bold'))
            else:
                btn = tk.Button(self, text=text, command=command, width=5, bd=0, highlightthickness=0, bg="darkgrey", font=("Terminal", 12, 'bold'))
            btn_window = self.create_window(x, y, window=btn)

    def open_file_menu(self):
        if self.file_menu is None:
            self.file_menu = tk.Menu(self, tearoff=0)
            self.file_menu.add_command(label="Open", command=self.main_window.open_file)
            self.file_menu.add_command(label="Save", command=self.main_window.save_file)
            self.file_menu.add_command(label="Save As", command=self.main_window.save_file_as)
            self.file_menu.add_command(label="New Window", command=self.main_window.new_window)
            self.file_menu.add_command(label="Exit", command=self.close_window)

        self.file_menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def open_edit_menu(self):
        if self.edit_menu is None:
            self.edit_menu = tk.Menu(self, tearoff=0)
            self.edit_menu.add_command(label="Copy", command=self.main_window.copy_text)
            self.edit_menu.add_command(label="Paste", command=self.main_window.paste_text)
            self.edit_menu.add_command(label="Delete", command=self.main_window.delete_text)
            self.edit_menu.add_command(label="Select All", command=self.main_window.select_all_text)

        self.edit_menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def open_theme_menu(self):
        if self.theme_menu is None:
            self.theme_menu = tk.Menu(self, tearoff=0)
            self.theme_menu.add_command(label="Light Theme", command=self.main_window.apply_light_theme)
            self.theme_menu.add_command(label="Dark Theme", command=self.main_window.apply_dark_theme)

        self.theme_menu.post(self.winfo_pointerx(), self.winfo_pointery())


