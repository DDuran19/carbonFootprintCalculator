import tkinter as tk
class TransparentFrame(tk.Toplevel):
    def __init__(self, master: tk.Frame):
        super().__init__(master)
        self.overrideredirect(True)  # Remove window decorations
        self.configure(bg='black')  # Set background color for the top widget
        self.geometry(f'800x550+{master.winfo_rootx()+50}+{master.winfo_rooty()+50}')  # Set position relative to the root window
        self.resizable(width=False,height=False)
        self.grid_propagate(0)