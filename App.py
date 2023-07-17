from typing import Callable, Optional, Tuple, Union
import customtkinter as CTk

class App(CTk.CTkTabview):
    def __init__(self, master, TABS, **kwargs):
        super().__init__(master, **kwargs)
        self.font = CTk.CTkFont(family="Helvetica", size=25)
        self.tabNames=TABS
        self.setup_tabs()
        self.tabs = self.winfo_children()

    def setup_tabs(self):
        self.setVehiclesFrame()

    def setVehiclesFrame(self):
        self.vehiclesFrame = self.add(self.tabNames[0])
        self.vehicleHeader = CTk.CTkLabel(self.vehiclesFrame,
            text="Which of the following vehicles do \nyou usually use on your commute?",
            font=self.font,)
        self.vehicleHeader.grid(row=0,column=0)
        self.vehicleBody = CTk.CTkFrame(self.vehiclesFrame)
        self.vehicleBody.grid(row=1,column=0)
        self.vehicleFooter = CTk.CTkFrame(self.vehiclesFrame)
        self.vehicleFooter.grid(row=2,column=0)
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
        
        self.motorcycleChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Motorcycle",variable=self.motorcycleChkVar, onvalue=True, offvalue=False)
        self.jeepneyChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Jeepney",variable=self.jeepneyChkVar, onvalue=True, offvalue=False)
        self.tricycleChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Tricycle",variable=self.tricycleChkVar, onvalue=True, offvalue=False)
        self.busChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Bus",variable=self.busChkVar, onvalue=True, offvalue=False)
        self.taxiChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Taxi",variable=self.taxiChkVar, onvalue=True, offvalue=False)
        self.SUVChkBox = CTk.CTkCheckBox(self.vehicleBody,text="SUV",variable=self.SUVChkVar, onvalue=True, offvalue=False)
        self.vanChkBox = CTk.CTkCheckBox(self.vehicleBody,text="Van ",variable=self.vanChkVar, onvalue=True, offvalue=False)

        self.motorcycleChkBox.grid(row=1, column=1,pady=(5,0), padx=(0,20))
        self.jeepneyChkBox.grid(row=2, column=1,pady=(5,0), padx=(0,20))
        self.tricycleChkBox.grid(row=3, column=1,pady=(5,0), padx=(0,20))
        self.busChkBox.grid(row=4, column=1,pady=(5,0), padx=(0,20))
        self.taxiChkBox.grid(row=1, column=2,pady=(5,0), padx=(0,20))
        self.SUVChkBox.grid(row=2, column=2,pady=(5,0), padx=(0,20))
        self.vanChkBox.grid(row=3, column=2,pady=(5,0), padx=(0,20))
            
    def setVehicleFooter(self):
        self.nextBtn = CTk.CTkButton(self.vehicleFooter,
            text="Next",
            command=self.submitVehicles)
        self.nextBtn.pack(side=CTk.BOTTOM)
    
    def submitVehicles(self):
        self.vehicles=[
            self.motorcycleChkVar.get(),
            self.jeepneyChkVar.get(),
            self.tricycleChkVar.get(),
            self.busChkVar.get(),
            self.taxiChkVar.get(),
            self.SUVChkVar.get(),
            self.vanChkVar.get()] 
        self.setTravelDetailsFrame()
        print(self.vehicles)

    def setTravelDetailsFrame(self):
        self.travelFrame = self.add(self.tabNames[1])
        self.set(self.tabNames[1])

        



    
class vehicle(CTk.CTkToplevel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    

if __name__ == "__main__":
    TABS: list = ["Vehicles", "Travel details", "Ownership", "Results"]

    app = CTk.CTk()
    app.app=App(app,TABS)
    app.app.pack()
    app.mainloop()