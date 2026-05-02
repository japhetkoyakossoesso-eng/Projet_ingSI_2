import tkinter as tk
# from tkinter import messagebox, ttk

from ui.theme import configure_theme


class AppController:
    def __init__(self, title: str, geometry: str) -> None:
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(geometry)
        self.root.minsize(1024, 520)

        configure_theme(self.root)

        # instructions


    def run(self) -> None:
        self.root.mainloop()
