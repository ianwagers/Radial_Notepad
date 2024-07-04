import tkinter as tk

class OuterBar(tk.Canvas):
    def __init__(self, master, radius, **kwargs):
        super().__init__(master, width=2*radius, height=2*radius, bg='lightgrey', **kwargs)
        self.master = master
        self.radius = radius
        self.create_oval(0, 0, 2*radius, 2*radius, outline='black', width=2)
        self.create_buttons()

    def create_buttons(self):
        button_size = 30
        pad = 10

        minimize_button = tk.Button(self, text="_", command=self.minimize_window, bd=0, bg='lightgrey')
        normalize_button = tk.Button(self, text="[]", command=self.normalize_window, bd=0, bg='lightgrey')
        close_button = tk.Button(self, text="X", command=self.close_window, bd=0, bg='red')

        minimize_button.place(x=self.radius - button_size - pad, y=pad, width=button_size, height=button_size)
        normalize_button.place(x=self.radius, y=pad, width=button_size, height=button_size)
        close_button.place(x=self.radius + button_size + pad, y=pad, width=button_size, height=button_size)

        file_button = tk.Button(self, text="File", bd=0, bg='lightgrey')
        edit_button = tk.Button(self, text="Edit", bd=0, bg='lightgrey')
        theme_button = tk.Button(self, text="Theme", bd=0, bg='lightgrey')

        file_button.place(x=self.radius - 60, y=2*self.radius - 40, width=50, height=20)
        edit_button.place(x=self.radius, y=2*self.radius - 40, width=50, height=20)
        theme_button.place(x=self.radius + 60, y=2*self.radius - 40, width=50, height=20)

    def minimize_window(self):
        self.master.iconify()

    def close_window(self):
        self.master.destroy()

    def normalize_window(self):
        self.master.state('normal')