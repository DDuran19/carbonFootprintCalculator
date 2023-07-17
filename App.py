from typing import Callable
from attr import dataclass
import customtkinter as CTk
import tkinter as tk
from tkinter import ttk
from utilities.calculations import VEHICLES

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
        print(self.vehicles)

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
        print(self.actualTravelDetails)
        for vehicle in self.actualTravelDetails:
            print("days: ",vehicle.days())

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


@dataclass
class Vehicle:
    name: str
    days: Callable[[], int]
    distance: Callable[[], int]

    

if __name__ == "__main__":
    TABS: list = ["Vehicles", "Travel details", "Ownership", "Results"]

    app = CTk.CTk()
    app.app=App(app,TABS, 'aquamarine')
    app.app.pack()
    app.mainloop()