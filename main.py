import os
import customtkinter as CTk
import tkinter as tk
import math
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image, ImageTk

from transparent import TransparentFrame
from utilities.calculations import CarbonFootprint
from introduction import intro
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


APPNAME: str = "Carbon Footprint Calculator"
CURRENTDIRECTORY:str = os.path.dirname(os.path.abspath(__file__))
MODE: str = CTk.get_appearance_mode()
DELETEICON:CTk.CTkImage = CTk.CTkImage(Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Delete.png"))
EDITICON:CTk.CTkImage = CTk.CTkImage(Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Edit.png"))

WHITE: str = "white"
BLACK: str = "black"
BACKGROUND_COLOR: str = BLACK
FOREGROUND_COLOR: str = BLACK

ENTER_KEY:str = "<Return>"
KEY_PRESS:str = '<KeyPress>'

TABS:list = ["Commute", "Vehicle", "Ownership", "Results"]
KM: int | None = None
L: int | None = None
FREQUENCY: float = 7
FUELTYPE: str | None = None
VEHICLE: str

class CarbonFootprintCalculator(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.setup_main_window()
        self.setup_widgets()

    def setup_main_window(self):
        self.background_image = Image.open("icons/background.jpg")
        self.background = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background)
        self.background_label.place(in_=self, x=0, y=0, relwidth=1, relheight=1)
        self.title(APPNAME)

        self.transparentFrame = TransparentFrame(self)
        self.transparentFrame.wm_attributes('-transparentcolor', BLACK)
        self.transparentFrame.lift()

        self.setup_main_window_sizes()
        self.setup_grids()
        CTk.set_appearance_mode("Light")

        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.transparentFrame.geometry(f'800x550+{self.winfo_rootx()}+{self.winfo_rooty()}')
        self.transparentFrame.lift()

    def setup_main_window_sizes(self):
        width = 800
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = math.floor((screen_width - width) / 2)
        y = math.floor((screen_height - height) / 2)
        alignStr = f"{width}x{height}+{x}+{y}"
        self.geometry(alignStr)
        self.resizable(width=False, height=False)

    def setup_grids(self):
        self.grid_rowconfigure(0)
        self.columnconfigure(0, weight=0, minsize=800)

    def setup_widgets(self):
        self.QuestionsFrame = QuestionsFrame(
            master=self.transparentFrame,
            width = 700,
            height = 500,
            depth=0,
            corner_radius=15,
            border_color=BLACK,
            border_width=2,
            command=self.tab_handler,
            bg_color=BLACK,
            fg_color=BLACK
        )

        self.QuestionsFrame.grid(row=0, column=0, sticky="nsew",padx = 50,pady=(30,0))

    def tab_handler(self):
        selected = self.QuestionsFrame.get()
        selected_index = TABS.index(selected)
        try: 
            for index, value in enumerate(TABS):
                if index > selected_index:
                    self.QuestionsFrame.delete(value)
        except ValueError:
            pass

class QuestionsFrame(CTk.CTkTabview):
    def __init__(self, master, depth, **kwargs):
        super().__init__(master, **kwargs)
        self.depth = depth
        self.font = CTk.CTkFont(family="Helvetica", size=25)
        self.setup_tabs()
        self.tabs = self.winfo_children()

    def setup_tabs(self):
        self.tab_commute()

    def tab_commute(self):
        parent = self.add(TABS[0])
        self.set(TABS[0])
        self.commute_frame = CTk.CTkFrame(master=parent, fg_color=FOREGROUND_COLOR, bg_color=BACKGROUND_COLOR)
        self.commute_frame.pack(side=CTk.TOP, pady=20, fill=CTk.X)
        self.commute_label = CTk.CTkLabel(master=self.commute_frame, text="How far (in Km) is your daily commute?", font=self.font)
        self.commute_label.pack(side=CTk.LEFT)
        self.commute_entry = CTk.CTkEntry(master=self.commute_frame)
        self.commute_entry.pack(side=CTk.RIGHT)

        self.commute_frame_days = CTk.CTkFrame(parent, fg_color=FOREGROUND_COLOR, bg_color=BACKGROUND_COLOR)
        self.commute_frame_days.pack(side=CTk.TOP, pady=20, fill=CTk.X)
        self.commute_label_days = CTk.CTkLabel(self.commute_frame_days, text="How often (in days) do you commute?", font=self.font)
        self.commute_label_days.pack(side=CTk.LEFT)
        self.commute_entry_days = CTk.CTkEntry(self.commute_frame_days)
        self.commute_entry_days.pack(side=CTk.RIGHT)
        days = CTk.StringVar(self.commute_entry_days, value="7")
        self.commute_entry_days.configure(textvariable=days)


        self.commute_nextBtn = CTk.CTkButton(parent, text="Next", command=self.tab_vehicle, state=(CTk.DISABLED if KM is None else CTk.NORMAL))
        self.commute_nextBtn.pack(side=CTk.BOTTOM)
        self.commute_entry.bind(ENTER_KEY, lambda event: self.validate_entry(event = event, entry=self.commute_entry, button=self.commute_nextBtn, command=self.tab_vehicle))
        self.commute_entry.bind(KEY_PRESS,lambda event: self.validate_entry(event = event, entry=self.commute_entry, button=self.commute_nextBtn))
    def tab_vehicle(self):
        parent = self.add(TABS[1])
        self.set(TABS[1])
        self.vehicle = ""
        self.vehicle_label = CTk.CTkLabel(
            parent,
            font=self.font,
            text="Which of the following vehicles are you using?",
        ).pack(side=CTk.TOP, pady=20)
        self.vehicle_option_menu = CTk.CTkOptionMenu(
            parent,
            command=self.tab_vehicle_select,
            values=[
                "Motorcycle",
                "Tricycle",
                "Jeepney",
                "Taxi",
                "Car-Hatchback",
                "Car-Sedan",
                "Car-SUV",
                "Pick-up",
                "Bus",
                "Van",
            ],
        )
        self.vehicle_option_menu.pack(side=CTk.TOP)

    def tab_vehicle_select(self, chosen):
        self.vehicle = chosen
        self.tab_ownership()

    def tab_ownership(self):
        parent = self.add(TABS[2])
        self.set(TABS[2])
        question = f"Do you own the {self.vehicle}?"
        self.ownership_frame = CTk.CTkFrame(
            parent, bg_color=BACKGROUND_COLOR, fg_color=FOREGROUND_COLOR
        )
        self.fuelType_frame = CTk.CTkFrame(
            parent, bg_color=BACKGROUND_COLOR, fg_color=FOREGROUND_COLOR
        )
        self.fuelUsage_frame = CTk.CTkFrame(
            parent, bg_color=BACKGROUND_COLOR, fg_color=FOREGROUND_COLOR
        )
        self.ownership_frame.pack(side=CTk.TOP, fill=CTk.X)

        self.ownership_label = CTk.CTkLabel(
            self.ownership_frame, text=question, font=self.font
        )
        self.ownership_option_menu = CTk.CTkOptionMenu(
            self.ownership_frame, values=["No", "Yes"], command=self.toggle_fuel_options
        )
        self.ownership_label.pack(side=CTk.LEFT, pady=(0, 20), padx=(0, 20))
        self.ownership_option_menu.pack(side=CTk.RIGHT, pady=(0, 20))

        self.fuelType_label = CTk.CTkLabel(
            master=self.fuelType_frame,
            font=self.font,
            text="What type of fuel are you using?",
        )
        self.fuel_type_option_menu = CTk.CTkOptionMenu(
            master=self.fuelType_frame, values=["Gasoline", "Diesel"]
        )

        self.fuel_usage_label = CTk.CTkLabel(
            master=self.fuelUsage_frame,
            font=self.font,
            text=f"Approximately how many liters of fuel \ndo you use in a week?",
            justify=CTk.LEFT,
            width=400,
        )
        self.fuel_usage_entry = CTk.CTkEntry(master=self.fuelUsage_frame, placeholder_text="type 0 if unsure")

        self.fuelType_label.pack(side=CTk.LEFT, pady=(0, 20), padx=(0, 20))
        self.fuel_type_option_menu.pack(side=CTk.RIGHT, pady=(0, 20))

        self.fuel_usage_label.pack(side=CTk.LEFT, pady=(0, 20), padx=(0, 20))
        self.fuel_usage_entry.pack(side=CTk.RIGHT, pady=(0, 20))
        self.ownership_nextBtn = CTk.CTkButton(
            parent, text="Next", command=self.tab_results, state=CTk.NORMAL)
        self.ownership_nextBtn.pack(side=CTk.BOTTOM)

        self.fuel_usage_entry.bind(ENTER_KEY, lambda event: self.validate_entry(event = event, entry=self.fuel_usage_entry,button=self.ownership_nextBtn, command=self.tab_results))
        self.fuel_usage_entry.bind(KEY_PRESS,lambda event: self.validate_entry(event = event, entry=self.fuel_usage_entry,button=self.ownership_nextBtn))

        # Initial state of ownership
        self.owner_state = False
        self.toggle_fuel_options("No")

    # This function will be called whenever the "ownership" dropdown value is changed.
    # Based on whether the ownership is 'Yes' or 'No', it either shows or hides the fuel usage input and label accordingly.
    def toggle_fuel_options(self, select):
        self.owner_state = True if select == "Yes" else False

        if self.owner_state:
            self.fuelType_frame.pack(side=CTk.TOP, fill=CTk.X)
            self.fuelUsage_frame.pack(side=CTk.TOP, fill=CTk.X)
            self.ownership_nextBtn.configure(state=(CTk.DISABLED if L is None else CTk.NORMAL))

        else:
            self.fuelType_frame.pack_forget()
            self.fuelUsage_frame.pack_forget()
            self.ownership_nextBtn.configure(state=CTk.NORMAL)

    def tab_results(self):
        parent = self.add(TABS[3])
        self.set(TABS[3])
        global KM
        global L
        global FREQUENCY
        global VEHICLE
        global FUELTYPE

        isOwned = self.ownership_option_menu.get()
        hasLiters = self.fuel_usage_entry.get()
        KM = int(self.commute_entry.get())
        FREQUENCY = int(self.commute_entry_days.get())
        VEHICLE = self.vehicle_option_menu.get()
        FUELTYPE = self.fuel_type_option_menu.get() if isOwned == "Yes" else None
        L = None if isOwned == "No" else int(hasLiters) if hasLiters else None

        self.carbonFootprint = CarbonFootprint(KM, VEHICLE, L, FREQUENCY, FUELTYPE)
        print(self.carbonFootprint.get_weekly_emission())
        print(self.carbonFootprint.get_monthly_emission())
        print(self.carbonFootprint.get_yearly_emission())
        weekly_emission = self.carbonFootprint.get_weekly_emission()
        monthly_emission = self.carbonFootprint.get_monthly_emission()
        yearly_emission = self.carbonFootprint.get_yearly_emission()

        # Create the data for the bar graph
        emission_types = ['Weekly', 'Monthly', 'Yearly']
        emission_values = [weekly_emission, monthly_emission, yearly_emission]

        value = {'Emission Period': emission_types, 'Emission Amount': emission_values}
        data = pd.DataFrame(value)

        self.figure = plt.Figure(figsize=(6,3))
        self.axes = self.figure.add_subplot(111)

        data.plot.bar(x='Emission Period', y='Emission Amount', ax=self.axes,edgecolor='black', color="#FF0000")
        self.axes.set_xticklabels(self.axes.get_xticklabels(), rotation=10)

        for rectangle in self.axes.patches:
            x = rectangle.get_x() + rectangle.get_width() / 2
            y = rectangle.get_height() / 2  
            count_value = int(rectangle.get_height())  
            self.axes.text(x, y, count_value, ha='center', va='center',color=WHITE)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=False) 
        # self.canvas.get_tk_widget().grid(row=0,column=0,padx=20,pady=20)


    def validate_entry(self, event, entry: CTk.CTkEntry, button: CTk.CTkButton, command = None):
        value = event.char
        try:
            float(entry.get())
            isFloat = True
        except ValueError:
            isFloat = False
        
        if value.isalpha() and value != "\x0D":
            button.configure(state=CTk.DISABLED)
        elif isFloat and command is not None:
            command()
        elif isFloat:
            button.configure(require_redraw = True, state = CTk.NORMAL)
        else: button.configure(state=CTk.DISABLED)
intro()
app = CarbonFootprintCalculator()
app.mainloop()
