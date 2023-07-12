import os
from typing import Optional, Tuple, Union
import customtkinter as CTk
import math
from PIL import Image

APPNAME: str = "Carbon Footprint Calculator"
CURRENTDIRECTORY = os.path.dirname(os.path.abspath(__file__))
MODE = CTk.get_appearance_mode()
DELETEICON = CTk.CTkImage(Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Delete.png"))
EDITICON = CTk.CTkImage(Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Edit.png"))


class CarbonFootprintCalculator(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_main_window()
        self.setup_widgets()

    def setup_main_window(self):
        self.title(APPNAME)
        self.setup_main_window_sizes()
        self.setup_grids()
        CTk.set_appearance_mode("Dark")
    def setup_main_window_sizes(self):
        width = 1020
        height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = math.floor((screen_width - width) / 2)
        y = math.floor((screen_height - height) / 2)
        alignStr = f"{width}x{height}+{x}+{y}"
        self.geometry(alignStr)
        self.resizable(width=False, height=False)
    def setup_grids(self):
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.columnconfigure(0, weight=0, minsize=50)
        self.columnconfigure(1, weight=0, minsize=620)
        self.columnconfigure(2, weight=0, minsize=50)
    def setup_widgets(self):
        self.CommuteDetailsFrame = CommuteDetailsFrame(
            master=self,
            corner_radius=15,
            border_color=("#0000FF", "#00FF00"),
            border_width=2,
        )
        self.CommuteDetailsFrame.grid(row=1, column=0, sticky="nsew")
        self.commuteScrollable = Scrollable(self.CommuteDetailsFrame)
        self.commuteScrollable.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.commutes = []

        self.btn_change_theme = CTk.CTkButton(
            master=self, command=self.change_theme, text="Change Theme"
        )
        self.btn_change_theme.grid(row=0, column=2)

        self.btn_add_commute = CTk.CTkButton(
            master=self, command=self.add_commute, text="Add"
        )
        self.btn_add_commute.grid(row=0, column=0)

        self.QuestionsFrame = QuestionsFrame(
            master=self, depth=2,
            corner_radius=15,
            border_color=("#0000FF", "#00FF00"),
            border_width=2,
        )
        self.QuestionsFrame.grid(row=1, column=1, sticky="nsew")

    def change_theme(self):
        global MODE
        if MODE == "Dark":
            CTk.set_appearance_mode("Light")
            MODE = "Light"
            self.update_icons()
            return
        CTk.set_appearance_mode("Dark")
        MODE = "Dark"
        self.update_icons()

    def update_icons(self):
        global DELETEICON
        DELETEICON = CTk.CTkImage(
            Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Delete.png")
        )

        commute: Commute
        for commute in self.commutes:
            commute.delete_btn.configure(require_redraw=True, image=DELETEICON)

    def add_commute(self):
        commute = Commute(self.commuteScrollable, "Home", 5, fg_color="transparent")
        commute.pack(anchor="w", padx=(1, 0), pady=1, fill="both")
        self.commutes.append(commute)


class Scrollable(CTk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class CommuteDetailsFrame(CTk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)


class Commute(CTk.CTkFrame):
    def __init__(self, master, Type, Km, **kwargs):
        super().__init__(master, **kwargs)
        self.type = Type
        self.value = Km
        self.label()
        self.delete_button()
        self.columnconfigure(0, weight=0, minsize=150)
        self.columnconfigure(1, weight=0)

    def label(self):
        self.label = CTk.CTkLabel(
            self, text=f"{self.type}: {self.value}Km", bg_color="transparent"
        )
        self.label.grid(row=0, column=0, sticky="w")

    def delete_button(self):
        self.delete_btn = CTk.CTkButton(
            self,
            text="",
            image=DELETEICON,
            width=25,
            fg_color="transparent",
            border_width=0,
            command=self.destroy,
        )
        self.delete_btn.grid(row=0, column=1, sticky="e")


class QuestionsFrame(CTk.CTkFrame):
    def __init__(self, master, depth, **kwargs):
        super().__init__(master, **kwargs)
        self.depth = depth
        self.setup_tabs()

    def setup_tabs(self):
        path = ["Commute", "Vehicle", "Ownership", "Fuel Type", "results"]
        self.tabs = CTk.CTkTabview(self)
        self.tabs.pack(fill = CTk.BOTH, expand=True)
        for i in range(self.depth+1):
            tab = self.tabs.add(path[i])

            if path[i] == "Commute":
                self.tab_commute(tab)
            elif path[i] == "Vehicle":
                self.tab_vehicle(tab)
            elif path[i] == "Ownership":
                self.tab_ownership(tab)
            elif path[i] == "Fuel Type":
                self.tab_fuelType(tab)

    # Commute Tab
    def tab_commute(self, parent):
        CTk.CTkLabel(parent, text='How far (in Km) is your daily commute?').grid(row=0, column=0)
        self.commute_entry = CTk.CTkEntry(parent)
        self.commute_entry.grid(row=1, column=0)

    def tab_vehicle(self, parent):
        CTk.CTkLabel(parent, text='Which of the following vehicles are you using?').grid(row=0, column=0)
        self.vehicle_option_menu = CTk.CTkOptionMenu(parent,values=
                                                    ['Motorcycle',
                                                    'Tricycle',
                                                    'Jeepney',
                                                    'Taxi',
                                                    'Car-Hatchback',
                                                    'Car-Sedan',
                                                    'Car-SUV',
                                                    'Pick-up',
                                                    'Bus',
                                                    'Van'])
        self.vehicle_option_menu.grid(row=0, column=1)
                                                    
    def tab_ownership(self, parent):
        CTk.CTkLabel(parent, text='Do you own the vehicle?').grid(row=0, column=0)
        self.ownership_option_menu = CTk.CTkOptionMenu(parent,values=
                                                        ['Yes',
                                                        'No'],
                                                        command=self.toggle_fuel_options)
        self.ownership_option_menu.grid(row=0, column=1)

        CTk.CTkLabel(parent, text='What type of fuel are you using?').grid(row=1, column=0)
        self.fuel_type_option_menu = CTk.CTkOptionMenu(parent, values=
                                                       ['Gasoline',
                                                       'Diesel'])
        self.fuel_type_option_menu.grid(row=1, column=1)
        
        self.fuel_usage_label = CTk.CTkLabel(parent, text=f'Approximately how many liters of  do you use in a day?')
        self.fuel_usage_label.grid(row=2, column=0)
        self.fuel_usage_entry = CTk.CTkEntry(parent)
        self.fuel_usage_entry.grid(row=2, column=1)
        
        # Initial state of ownership
        self.owner_state = False
        self.toggle_fuel_options('No')

    def tab_fuelType(self, parent):
        #write code here
        pass                                             
  
    # This function will be called whenever the "ownership" dropdown value is changed.
    # Based on whether the ownership is 'Yes' or 'No', it either shows or hides the fuel usage input and label accordingly.
    def toggle_fuel_options(self, select):  
        self.owner_state = True if select == 'Yes' else  False

        if self.owner_state:
            self.fuel_type_option_menu.grid()
            self.fuel_usage_label.grid()
            self.fuel_usage_entry.grid()
        else:
            self.fuel_type_option_menu.grid_remove()
            self.fuel_usage_label.grid_remove()
            self.fuel_usage_entry.grid_remove()


class CommuteQuestionFrame(CTk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

app = CarbonFootprintCalculator()
app.mainloop()
