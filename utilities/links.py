import tkinter as tk
from tkinter import ttk
import subprocess
from typing import Literal, Optional, Tuple, Union
from typing_extensions import Literal
import customtkinter as CTk
from customtkinter.windows.widgets.font import CTkFont

class Thumbnail(ttk.Frame):
    def __init__(self, parent, thumbnail_image, description, url):
        super().__init__(parent)
        self.thumbnail_image = thumbnail_image
        self.description = description
        self.url = url

        # Create a thumbnail button with an image
        self.thumbnail_button = ttk.Button(self, image=self.thumbnail_image, command=self.open_webview)
        self.thumbnail_button.pack(side=tk.LEFT)

        # Create a description label
        self.description_label = ttk.Label(self, text=self.description)
        self.description_label.pack(side=tk.RIGHT)

    def open_webview(self):
        subprocess.run(["python", "assets/webViewer.py", self.url], creationflags=subprocess.CREATE_NO_WINDOW)

class Links(CTk.CTkScrollableFrame):

    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, scrollbar_fg_color: str | Tuple[str, str] | None = None, scrollbar_button_color: str | Tuple[str, str] | None = None, scrollbar_button_hover_color: str | Tuple[str, str] | None = None, label_fg_color: str | Tuple[str, str] | None = None, label_text_color: str | Tuple[str, str] | None = None, label_text: str = "", label_font: tuple | CTkFont | None = None, label_anchor: str = "center", orientation: Literal['vertical', 'horizontal'] = "vertical"):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, scrollbar_fg_color, scrollbar_button_color, scrollbar_button_hover_color, label_fg_color, label_text_color, label_text, label_font, label_anchor, orientation)
        self.createThumbnails()
   
    
    def createThumbnails(self):
        # Create the thumbnails and descriptions
        thumbnail1 = tk.PhotoImage(file="assets/CarbonEmissions.png").subsample(7)
        description1 = "What is Carbon Emissions"
        url1 = "CarbonEmissions.html"
        Thumbnail(self, thumbnail_image=thumbnail1, description=description1, url=url1).pack(side=tk.TOP, padx=5, pady=10)

        thumbnail2 = tk.PhotoImage(file="assets/CarbonFootprintForKids.png").subsample(7)
        description2 = "Carbon Footprint For Kids"
        url2 = "CarbonFootprintForKids.html"
        Thumbnail(self, thumbnail_image=thumbnail2, description=description2, url=url2).pack(side=tk.TOP, padx=5, pady=10)

        thumbnail3 = tk.PhotoImage(file="assets/MoreOnCarbonEmission.png").subsample(7)
        description3 = "More on Carbon Emissions"
        url3 = "MoreOnCarbonEmission.html"
        Thumbnail(self, thumbnail_image=thumbnail3, description=description3, url=url3).pack(side=tk.TOP, padx=5, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Learn More Resources")

    links_frame = Links(root)
    links_frame.pack()

    links_frame.mainloop()
