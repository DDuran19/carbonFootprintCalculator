import os, subprocess
import customtkinter as CTk
import tkinter as tk
import math
import pandas as pd
import matplotlib.pyplot as plt
import colorsys

from typing import Callable
from attr import dataclass
from PIL import Image, ImageTk
from tkinter import ttk
from transparent import TransparentFrame
from utilities.calculations import CarbonFootprint, VEHICLES
from utilities.results import CircularProgressBar
from utilities.links import Links
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data.dataProcessor import DataProcessor
from App import App

APPNAME: str = "Carbon Footprint Calculator"
CURRENTDIRECTORY: str = os.path.dirname(os.path.abspath(__file__))
MODE: str = CTk.get_appearance_mode()
DELETEICON: CTk.CTkImage = CTk.CTkImage(
    Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Delete.png")
)
EDITICON: CTk.CTkImage = CTk.CTkImage(
    Image.open(f"{CURRENTDIRECTORY}/icons/{MODE}Edit.png")
)

WHITE: str = "white"
TRANSPARENT: str = "gray"
BACKGROUND_COLOR: str = "black"
FOREGROUND_COLOR: str = "black"

ENTER_KEY: str = "<Return>"
KEY_PRESS: str = "<KeyPress>"

TABS: list = ["Commute", "Vehicle", "Results"]
KM: int = 0
L: int  = 0
KGCO2perLperWeek: float = 0
KGCO2perKmperWeek: float = 0


class CarbonFootprintCalculator(CTk.CTk):
    """
    This class represents the main application window for the Carbon Footprint Calculator.

init(): Initializes the CarbonFootprintCalculator class by calling the superclass constructor and setting up the main window. It also sets up the widgets for the application.

setup_main_window(): Sets up the main window of the application by creating a background image, transparent frame, and configuring the window size and appearance.

on_configure(event): Callback function that is triggered when the window is resized. It adjusts the position and size of the transparent frame to match the main window.

setup_main_window_sizes(): Sets up the size and position of the main window based on the screen dimensions.

setup_grids(): Configures the grid layout of the main window.

setup_widgets(): Sets up the widgets within the main window, including the QuestionsFrame.

tab_handler(): Handles the tab switching logic when a tab is selected in the QuestionsFrame.

QuestionsFrame: This class represents the frame that contains the different tabs for the questions in the application.

init(master, **kwargs): Initializes the QuestionsFrame class by calling the superclass constructor and setting up the tabs and their respective widgets.

setup_tabs(): Sets up the different tabs in the QuestionsFrame.

tab_commute(): Sets up the "Commute" tab, which includes the widgets for entering the daily commute distance and commute frequency.

tab_vehicle(): Sets up the "Vehicle" tab, which includes the widget for selecting the type of vehicle.

tab_vehicle_select(chosen): Callback function that is triggered when a vehicle is selected in the dropdown menu. It sets the selected vehicle and proceeds to the next tab.

tab_ownership(): Sets up the "Ownership" tab, which includes the widgets for selecting ownership status and fuel type.

toggle_fuel_options(select): Callback function that is triggered when the ownership dropdown value is changed. It shows or hides the fuel usage input and label based on the ownership status.

tab_results(): Sets up the "Results" tab, which includes the carbon footprint results and a bar chart comparing the user's emissions to other countries.

tips(percentage, parent): Displays the carbon footprint results in a separate top-level window, including a circular progress bar, rating, and resource links.

generate_hex_color(value): Generates a hexadecimal color code based on a given value, which is used to determine the color of the circular progress bar.

generate_rating(percentage): Generates a rating and response based on the user's carbon footprint percentage.

validate_entry(event, entry, button, command=None): Validates the input in an entry field and enables or disables a button based on the input.


    """
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
        self.transparentFrame.wm_attributes("-transparentcolor", TRANSPARENT)
        self.transparentFrame.lift()

        self.setup_main_window_sizes()
        self.setup_grids()
        CTk.set_appearance_mode("Light")

        self.bind("<Configure>", self.on_configure)

    def on_configure(self, event):
        self.transparentFrame.geometry(
            f"800x550+{self.winfo_rootx()}+{self.winfo_rooty()}"
        )
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
        self.QuestionsFrame = App(
            master=self.transparentFrame,
            TABS=TABS,
            defaultcolor=TRANSPARENT,
            width=700,
            height=500,
            border_color=TRANSPARENT,
            border_width=2,
            command=self.tab_handler,
            bg_color=TRANSPARENT,
            fg_color=TRANSPARENT,
        )

        # self.QuestionsFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(30, 0))
        self.QuestionsFrame.pack(fill=CTk.X)
    def tab_handler(self):
        selected = self.QuestionsFrame.get()
        selected_index = TABS.index(selected)
        
        global KM
        global L
        global KGCO2perKmperWeek
        global KGCO2perLperWeek
        
        try:
            for index, value in enumerate(TABS):
                if index > selected_index:
                    self.QuestionsFrame.delete(value)
                    KM = 0
                    L  = 0
                    KGCO2perLperWeek = 0
                    KGCO2perKmperWeek = 0
                 
        except ValueError:
            pass


class QuestionsFrame(CTk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTk.CTkFont(family="Helvetica", size=25)
        self.setup_tabs()
        self.tabs = self.winfo_children()

    def setup_tabs(self):
        self.tab_commute()

    def tab_commute(self):
        parent = self.add(TABS[0])
        self.set(TABS[0])
        self.commute_frame = CTk.CTkFrame(
            master=parent, fg_color=TRANSPARENT, bg_color=TRANSPARENT
        )
        self.commute_frame.pack(side=CTk.TOP, pady=20, fill=CTk.X)
        self.commute_label = CTk.CTkLabel(
            master=self.commute_frame,
            text="How far (in Km) is your daily commute?",
            font=self.font,
        )
        self.commute_label.pack(side=CTk.LEFT)
        self.commute_entry = CTk.CTkEntry(master=self.commute_frame)
        self.commute_entry.pack(side=CTk.RIGHT)

        self.commute_frame_days = CTk.CTkFrame(
            parent, fg_color=TRANSPARENT, bg_color=TRANSPARENT
        )
        self.commute_frame_days.pack(side=CTk.TOP, pady=20, fill=CTk.X)
        self.commute_label_days = CTk.CTkLabel(
            self.commute_frame_days,
            text="How often (in days) do you commute?",
            font=self.font,
        )
        self.commute_label_days.pack(side=CTk.LEFT)
        self.commute_entry_days = CTk.CTkEntry(self.commute_frame_days)
        self.commute_entry_days.pack(side=CTk.RIGHT)
        days = CTk.StringVar(self.commute_entry_days, value="7")
        self.commute_entry_days.configure(textvariable=days)

        self.commute_nextBtn = CTk.CTkButton(
            parent,
            text="Next",
            command=self.tab_vehicle,
            state=(CTk.DISABLED if KM is None else CTk.NORMAL),
        )
        self.commute_nextBtn.pack(side=CTk.BOTTOM)
        self.commute_entry.bind(
            ENTER_KEY,
            lambda event: self.validate_entry(
                event=event,
                entry=self.commute_entry,
                button=self.commute_nextBtn,
                command=self.tab_vehicle,
            ),
        )
        self.commute_entry.bind(
            KEY_PRESS,
            lambda event: self.validate_entry(
                event=event, entry=self.commute_entry, button=self.commute_nextBtn
            ),
        )

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
            parent, bg_color=TRANSPARENT, fg_color=TRANSPARENT
        )
        self.fuelType_frame = CTk.CTkFrame(
            parent, bg_color=TRANSPARENT, fg_color=TRANSPARENT
        )
        self.fuelUsage_frame = CTk.CTkFrame(
            parent, bg_color=TRANSPARENT, fg_color=TRANSPARENT
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
        self.fuel_usage_entry = CTk.CTkEntry(
            master=self.fuelUsage_frame, placeholder_text="type 0 if unsure"
        )

        self.fuelType_label.pack(side=CTk.LEFT, pady=(0, 20), padx=(0, 20))
        self.fuel_type_option_menu.pack(side=CTk.RIGHT, pady=(0, 20))

        self.fuel_usage_label.pack(side=CTk.LEFT, pady=(0, 20), padx=(0, 20))
        self.fuel_usage_entry.pack(side=CTk.RIGHT, pady=(0, 20))
        self.ownership_nextBtn = CTk.CTkButton(
            parent, text="Next", command=self.tab_results, state=CTk.NORMAL
        )
        self.ownership_nextBtn.pack(side=CTk.BOTTOM)

        self.fuel_usage_entry.bind(
            ENTER_KEY,
            lambda event: self.validate_entry(
                event=event,
                entry=self.fuel_usage_entry,
                button=self.ownership_nextBtn,
                command=self.tab_results,
            ),
        )
        self.fuel_usage_entry.bind(
            KEY_PRESS,
            lambda event: self.validate_entry(
                event=event, entry=self.fuel_usage_entry, button=self.ownership_nextBtn
            ),
        )

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
            self.ownership_nextBtn.configure(
                state=(CTk.DISABLED if L is None else CTk.NORMAL)
            )

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
        weekly_emission = self.carbonFootprint.get_weekly_emission()
        monthly_emission = self.carbonFootprint.get_monthly_emission()
        yearly_emission = self.carbonFootprint.get_yearly_emission()

        raw = DataProcessor()
        data = raw.get_ranking(weekly_emission)

        # Define colors for the bar chart
        color_map = plt.get_cmap("Blues")
        colors = [color_map(1 - (i / (len(data) - 1))) for i in range(len(data))]

        # Set the color for "Your Footprint" to green
        colors[data.index.get_loc("Your Footprint")] = "green"

        self.figure = plt.Figure(figsize=(6, 3))
        self.axes = self.figure.add_subplot(111)

        bars = data.plot.bar(
            x="Country", y="KgCO2perWeek", ax=self.axes, edgecolor="black", color=colors
        )

        # Set the font color for "Your Footprint" to red
        bars.get_xticklabels()[data.index.get_loc("Your Footprint")].set_color("red")

        self.axes.set_xticklabels(self.axes.get_xticklabels(), rotation=10)

        # Add labels for the bar heights
        for rectangle in self.axes.patches:
            x = rectangle.get_x() + rectangle.get_width() / 2
            y = rectangle.get_height() / 2
            count_value = int(rectangle.get_height())
            self.axes.text(
                x,
                y,
                count_value,
                ha="center",
                va="center",
                color="black",
                bbox={"facecolor": "white", "edgecolor": "none"},
            )

        self.figure.tight_layout()  # Automatically adjusts the layout to fit the figure within the parent container

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tips(raw.get_percentage(), parent)

    def tips(self, percentage, parent):
        descriptionFont = CTk.CTkFont(family="Helvetica", size=12, weight="bold")
        ratingFont = CTk.CTkFont(family="Helvetica", size=12)

        top_level = CTk.CTkToplevel(parent, fg_color=WHITE)
        top_level.resizable(False,False)
        top_level.title("Carbon Footprint Results")
        top_level.geometry(f"400x600+{self.master.winfo_rootx()+self.winfo_width()-3}+{self.master.winfo_rooty()-30}")
        formatted_percentage = format(100 * percentage, ".2f")
        percentage *= 100
        color = self.generate_hex_color(percentage)
        rating = self.generate_rating(percentage)

        self.canvas = CTk.CTkCanvas(
            top_level, width=200, height=200, background=WHITE, highlightthickness=0
        )
        self.canvas.place(x=0, y=0)
        self.progress = CircularProgressBar(
            self.canvas, percentage=percentage, color=color, rating=rating[0]
        )
        description_label = CTk.CTkLabel(
            top_level,
            text=f"Your footprint rating: {formatted_percentage}%",
            font=descriptionFont,
            justify=CTk.LEFT,
            width=195,
            wraplength=200
        )
        description_label.place(x=200, y=30)
        rating_label = CTk.CTkLabel(
            top_level,
            text=rating[1],
            font=ratingFont,
            justify=CTk.LEFT,
            width=195,
            wraplength=200
        )
        
        label = CTk.CTkLabel(top_level, text="Check out these resources to learn more!", font=("Helvetica", 12, "bold"))
        label.place(x=20,y=190)
        rating_label.place(x=200, y=70)
        self.links = Links(top_level,fg_color=WHITE,bg_color=WHITE,width=400, height=400)
        self.links.place(x=0,y=210)


    def generate_hex_color(self, value):
        if value == 100:
            return "#FF0000"
        normalized_value = value / 100
        hue = (120 - (normalized_value * 120)) / 360
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255)
        )

        return hex_color

    def generate_rating(self, percentage):
        if percentage > 80:
            rating = "VERY BAD"
            response = "Your carbon footprint emission is very high. It is crucial to take immediate action to reduce your emissions and adopt more sustainable practices."
        elif percentage > 60:
            rating = "Bad"
            response = "Your carbon footprint emission is high. Consider implementing changes in your lifestyle and habits to lower your emissions and contribute to a greener environment."
        elif percentage > 50:
            rating = "Average"
            response = "Your carbon footprint emission is at an average level. There is still room for improvement in reducing your emissions and embracing more eco-friendly choices."
        elif percentage < 5:
            rating = "Excellent!"
            response = "Congratulations! Your carbon footprint emission is extremely low. You are making a significant positive impact on the environment with your sustainable practices."
        elif percentage < 15:
            rating = "Very Good"
            response = "Great job! Your carbon footprint emission is very low. Continue practicing sustainable behaviors to further reduce your emissions and protect the planet."
        elif percentage < 30:
            rating = "Good"
            response = "Your carbon footprint emission is good. Keep up the efforts to lower your emissions and strive for even better sustainability practices."
        else:
            rating = "Unknown"
            response = "We couldn't determine an appropriate response for your carbon footprint emission score. Please consult with a specialist for further evaluation."
        return rating, response

    def validate_entry(
        self, event, entry: CTk.CTkEntry, button: CTk.CTkButton, command=None
    ):
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
            button.configure(require_redraw=True, state=CTk.NORMAL)
        else:
            button.configure(state=CTk.DISABLED)


class App(CTk.CTkTabview):
    def __init__(self, master, TABS, defaultcolor, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTk.CTkFont(family="Helvetica", size=35)
        self.tabNames=TABS
        self.defaultColor = defaultcolor
        self.setup_tabs()
        self.tabs = self.winfo_children()

    def setup_tabs(self):
        self.setVehiclesFrame()

    def setVehiclesFrame(self):
        self.vehiclesFrame = self.add(self.tabNames[0])
        self.vehicleHeader = CTk.CTkLabel(self.vehiclesFrame,
            text="Which of the following vehicles do \nyou usually use on your commute?",
            font=self.font)
        # self.vehicleHeader.grid(row=0,column=1)
        self.vehicleHeader.pack(side=CTk.TOP, fill=CTk.X, pady=(0,20))
        self.vehicleBody = CTk.CTkFrame(self.vehiclesFrame,       
            fg_color=self.defaultColor,
            bg_color=self.defaultColor)
        # self.vehicleBody.grid(row=1,column=1)
        self.vehicleBody.pack(side=CTk.TOP, fill=CTk.X, padx=150)
        self.vehicleBody.columnconfigure(1,minsize=300)
        self.vehicleFooter = CTk.CTkFrame(self.vehiclesFrame,       
            fg_color=self.defaultColor,
            bg_color=self.defaultColor)
        # self.vehicleFooter.grid(row=2,column=1)
        self.vehicleFooter.pack(side=CTk.TOP, fill=CTk.X, padx=150)
        self.setVehicleFooter()
        self.setVehicleBody()
    
    def setVehicleBody(self):
        
        self.motorcycleChkVar = CTk.BooleanVar(value=False)
        self.jeepneyChkVar = CTk.BooleanVar(value=False)
        self.tricycleChkVar = CTk.BooleanVar(value=False)
        self.busChkVar = CTk.BooleanVar(value=False)
        self.taxiChkVar = CTk.BooleanVar(value=False)
        self.SUVChkVar = CTk.BooleanVar(value=False)
        self.vanChkVar = CTk.BooleanVar(value=False)  
        
        self.motorcycleChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Motorcycle",font=self.font, variable=self.motorcycleChkVar, onvalue=True, offvalue=False)
        self.jeepneyChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Jeepney",font=self.font, variable=self.jeepneyChkVar, onvalue=True, offvalue=False)
        self.tricycleChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Tricycle",font=self.font, variable=self.tricycleChkVar, onvalue=True, offvalue=False)
        self.busChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Bus",font=self.font, variable=self.busChkVar, onvalue=True, offvalue=False)
        self.taxiChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Taxi",font=self.font, variable=self.taxiChkVar, onvalue=True, offvalue=False)
        self.SUVChkBox = CTk.CTkCheckBox(self.vehicleBody,text="SUV",font=self.font, variable=self.SUVChkVar, onvalue=True, offvalue=False)
        self.vanChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Van ",font=self.font, variable=self.vanChkVar, onvalue=True, offvalue=False)

        self.motorcycleChkBox.grid(row=1, column=1, pady=(0,20),sticky=CTk.W)
        self.jeepneyChkBox.grid(row=2, column=1, pady=(0,20),sticky=CTk.W)
        self.tricycleChkBox.grid(row=3, column=1, pady=(0,20),sticky=CTk.W)
        self.busChkBox.grid(row=4, column=1, pady=(0,20),sticky=CTk.W)
        self.taxiChkBox.grid(row=1, column=2, sticky=CTk.W)
        self.SUVChkBox.grid(row=2, column=2, sticky=CTk.W)
        self.vanChkBox.grid(row=3, column=2, sticky=CTk.W)
            
    def setVehicleFooter(self):
        self.nextBtn = CTk.CTkButton(self.vehicleFooter,
            text="Next",
            command=self.submitVehicles)
        self.nextBtn.pack(side=CTk.BOTTOM)
    
    def submitVehicles(self):
        self.vehicles={
            "Motorcycle": self.motorcycleChkVar.get(),
            "Jeepney": self.jeepneyChkVar.get(),
            "Tricycle": self.tricycleChkVar.get(),
            "Bus": self.busChkVar.get(),
            "Taxi": self.taxiChkVar.get(),
            "SUV": self.SUVChkVar.get(),
            "Van": self.vanChkVar.get()}
        self.setTravelDetailsFrame()

    def setTravelDetailsFrame(self):
        self.travelFrame = self.add(self.tabNames[1])
        self.set(self.tabNames[1])
        self.actualTravelDetails = []
        for k, v in self.vehicles.items():
            if v:
                frame = self.setVehicle(self.travelFrame, k)
                self.actualTravelDetails.append(
                    Vehicle(k, frame.days_var.get, frame.distance_var.get)
                    )
        self.nextBtn2 = CTk.CTkButton(self.travelFrame,
            text="Next",
            command=self.tab_results)
        self.nextBtn2.pack(side=CTk.BOTTOM)

    def setVehicle(self, travelFrame, vehicleName):
        row = CTk.CTkFrame(travelFrame, border_color="black",border_width=2)
        row.pack(pady=5)
        
        # Vehicle Name
        vehicle_label = CTk.CTkLabel(row, text=vehicleName)
        vehicle_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Days Dropdown
        values=["1","2","3","4","5","6","7"]
        row.days_var = CTk.IntVar(row,value=1)
        days_dropdown = CTk.CTkOptionMenu(row, variable=row.days_var,values=values,  width=2)
        days_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Distance Entry
        def validate_distance(text:str):
            if text.isdigit() or text == "":
                print('valid')
                return True
            else:
                print("invalid")
                return False
        
        row.distance_var = CTk.StringVar(row,value="")
        distance_entry = tk.Entry(row, textvariable=row.distance_var, width=4, justify='right')
        distance_entry['validate'] = 'key'
        distance_entry['validatecommand'] = (distance_entry.register(validate_distance), '%P')
        distance_entry.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        row.columnconfigure(0,minsize=300)
        return row



    def tab_results(self):
        parent = self.add(TABS[2])
        self.set(TABS[2])
        global KM
        global L
        global KGCO2perLperWeek
        global KGCO2perKmperWeek

        for vehicle in self.actualTravelDetails:
            distance = int(vehicle.distance()) * int(vehicle.days())
            fuelEfficiency = VEHICLES[vehicle.name]['KmperL'] 
            fuelFactor = VEHICLES[vehicle.name]['defaultFuel'] 
            vehicleFactor = VEHICLES[vehicle.name]['KgCO2perKm']
            KM += distance
            L += distance/fuelEfficiency
            KGCO2perLperWeek+= fuelFactor * L
            KGCO2perKmperWeek+= vehicleFactor * KM

        self.carbonFootprint = CarbonFootprint(KM, L, KGCO2perLperWeek, KGCO2perKmperWeek )
        weekly_emission = self.carbonFootprint.get_weekly_emission()
        monthly_emission = self.carbonFootprint.get_monthly_emission()
        yearly_emission = self.carbonFootprint.get_yearly_emission()

        raw = DataProcessor()
        data = raw.get_ranking(weekly_emission)

        # Define colors for the bar chart
        color_map = plt.get_cmap("Blues")
        colors = [color_map(1 - (i / (len(data) - 1))) for i in range(len(data))]

        # Set the color for "Your Footprint" to green
        colors[data.index.get_loc("Your Footprint")] = "green"

        self.figure = plt.Figure(figsize=(6, 3))
        self.axes = self.figure.add_subplot(111)

        bars = data.plot.bar(
            x="Country", y="KgCO2perWeek", ax=self.axes, edgecolor="black", color=colors
        )

        # Set the font color for "Your Footprint" to red
        bars.get_xticklabels()[data.index.get_loc("Your Footprint")].set_color("red")

        self.axes.set_xticklabels(self.axes.get_xticklabels(), rotation=10)

        # Add labels for the bar heights
        for rectangle in self.axes.patches:
            x = rectangle.get_x() + rectangle.get_width() / 2
            y = rectangle.get_height() / 2
            count_value = int(rectangle.get_height())
            self.axes.text(
                x,
                y,
                count_value,
                ha="center",
                va="center",
                color="black",
                bbox={"facecolor": "white", "edgecolor": "none"},
            )

        self.figure.tight_layout()  # Automatically adjusts the layout to fit the figure within the parent container

        self.canvas = FigureCanvasTkAgg(self.figure, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.tips(raw.get_percentage(), parent)

    def tips(self, percentage, parent):
        descriptionFont = CTk.CTkFont(family="Helvetica", size=12, weight="bold")
        ratingFont = CTk.CTkFont(family="Helvetica", size=12)

        top_level = CTk.CTkToplevel(parent, fg_color=WHITE)
        top_level.resizable(False,False)
        top_level.title("Carbon Footprint Results")
        top_level.geometry(f"400x600+{self.master.winfo_rootx()+self.winfo_width()-3}+{self.master.winfo_rooty()-30}")
        formatted_percentage = format(100 * percentage, ".2f")
        percentage *= 100
        color = self.generate_hex_color(percentage)
        rating = self.generate_rating(percentage)

        self.canvas = CTk.CTkCanvas(
            top_level, width=200, height=200, background=WHITE, highlightthickness=0
        )
        self.canvas.place(x=0, y=0)
        self.progress = CircularProgressBar(
            self.canvas, percentage=percentage, color=color, rating=rating[0]
        )
        description_label = CTk.CTkLabel(
            top_level,
            text=f"Your footprint rating: {formatted_percentage}%",
            font=descriptionFont,
            justify=CTk.LEFT,
            width=195,
            wraplength=200
        )
        description_label.place(x=200, y=30)
        rating_label = CTk.CTkLabel(
            top_level,
            text=rating[1],
            font=ratingFont,
            justify=CTk.LEFT,
            width=195,
            wraplength=200
        )
        
        label = CTk.CTkLabel(top_level, text="Check out these resources to learn more!", font=("Helvetica", 12, "bold"))
        label.place(x=20,y=190)
        rating_label.place(x=200, y=70)
        self.links = Links(top_level,fg_color=WHITE,bg_color=WHITE,width=400, height=400)
        self.links.place(x=0,y=210)


    def generate_hex_color(self, value):
        if value == 100:
            return "#FF0000"
        normalized_value = value / 100
        hue = (120 - (normalized_value * 120)) / 360
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

        hex_color = "#{:02x}{:02x}{:02x}".format(
            int(r * 255), int(g * 255), int(b * 255)
        )

        return hex_color

    def generate_rating(self, percentage):
        if percentage > 80:
            rating = "VERY BAD"
            response = "Your carbon footprint emission is very high. It is crucial to take immediate action to reduce your emissions and adopt more sustainable practices."
        elif percentage > 60:
            rating = "Bad"
            response = "Your carbon footprint emission is high. Consider implementing changes in your lifestyle and habits to lower your emissions and contribute to a greener environment."
        elif percentage > 50:
        
            rating = "Average"
            response = "Your carbon footprint emission is at an average level. There is still room for improvement in reducing your emissions and embracing more eco-friendly choices."
        
        elif percentage > 30:
            rating = "Good"
            response = "Your carbon footprint emission is good. Keep up the efforts to lower your emissions and strive for even better sustainability practices."
        
        elif percentage > 15:
            rating = "Very Good"
            response = "Great job! Your carbon footprint emission is very low. Continue practicing sustainable behaviors to further reduce your emissions and protect the planet."
        
        elif percentage > 5:
            rating = "Excellent!"
            response = "Congratulations! Your carbon footprint emission is extremely low. You are making a significant positive impact on the environment with your sustainable practices."

        elif percentage > 0:
            rating = "Superb!"
            response = "You are a role model for your dedication in reducing your carbon footprint. Keep up the great work and continue to inspire others to make sustainable choices. Together, we can create a greener future for our planet!"

        return rating, response

    def validate_entry(
        self, event, entry: CTk.CTkEntry, button: CTk.CTkButton, command=None
    ):
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
            button.configure(require_redraw=True, state=CTk.NORMAL)
        else:
            button.configure(state=CTk.DISABLED)
@dataclass
class Vehicle:
    name: str
    days: Callable[[], int]
    distance: Callable[[], int]

    









subprocess.run(["python", "./assets/introduction.py"], creationflags=subprocess.CREATE_NO_WINDOW)
app = CarbonFootprintCalculator()
app.mainloop()
