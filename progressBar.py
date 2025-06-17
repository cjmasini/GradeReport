import tkinter as tk
from tkinter import ttk

class ProgressBar:
    def __init__(self, parent, row, columnspan=2):
        self.frame = tk.Frame(parent, bg="#f8f9fa")
        self.frame.grid(row=row, column=0, columnspan=columnspan, sticky="ew", padx=20)

        self.progress = ttk.Progressbar(
            self.frame, orient="horizontal", length=300, mode="determinate"
        )
        self.progress.pack(padx=10, pady=5)

    def update(self, value):
        self.progress["value"] = value
        self.progress.update_idletasks()

    def hide(self):
        self.frame.grid_remove()

    def show(self):
        self.frame.grid()
