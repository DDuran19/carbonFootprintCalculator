import json

with open("data.json", "r") as file:
    VEHICLES = json.load(file)

        # self.carbonFootprint = CarbonFootprint(KM, L, KGCO2perLperWeek)

class CarbonFootprint:
    def __init__(
        self,
        distance: float,
        fuel: float | None = None,
        KGCO2perLperWeek: float | None = None,
        KGCO2perKmperWeek: float | None = None
    ) -> None:
        self.distance = distance
        self.fuel = fuel
        self.KGCO2perLperWeek = KGCO2perLperWeek
        self.KGCO2perKmperWeek = KGCO2perKmperWeek
    def get_weekly_emission(self):
        return self.KGCO2perLperWeek + self.KGCO2perKmperWeek

    def get_monthly_emission(self):
        return self.get_weekly_emission() * 4

    def get_yearly_emission(self):
        return self.get_weekly_emission() * 52
