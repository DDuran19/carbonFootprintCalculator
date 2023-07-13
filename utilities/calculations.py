import json

with open("data.json", "r") as file:
    VEHICLES = json.load(file)

class CarbonFootprint:
    def __init__(
        self,
        distance: float,
        vehicle: str,
        fuel: float | None = None,
        frequency: float = 7,
        fuelType: str | None = None,
    ) -> None:
        self.distance = distance
        self.frequency = frequency
        self.vehicle = VEHICLES[vehicle]
        self.fuelType = (
            None if fuelType is None else (2.175 if fuelType == "Gasoline" else 2.556)
        )
        self.fuel = fuel

    def get_weekly_emission(self):
        Lperweek = (self.fuel if self.fuel is not None else (self.distance * (1 / self.vehicle["KmperL"])))
        
        KgCO2perL = Lperweek * (
            self.vehicle["defaultFuel"] if self.fuelType is None else self.fuelType
        )
        KgCO2perKm = self.vehicle["KgCO2perKm"] * self.distance
        return KgCO2perL + KgCO2perKm

    def get_monthly_emission(self):
        return self.get_weekly_emission() * 4

    def get_yearly_emission(self):
        return self.get_weekly_emission() * 52
