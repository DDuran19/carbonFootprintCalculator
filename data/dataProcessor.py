import pandas as pd
LOCATION = "data/worldEmissionData.csv"
class DataProcessor:

    def __init__(self, csv_file=LOCATION):
        self.df:pd.DataFrame = pd.read_csv(csv_file).set_index("Country")

    def get_KgCO2perWeek(self, sorted: bool = False):
        if sorted:
            return self.df['KgCO2perWeek'].sort_values(ascending=False)
        return self.df['KgCO2perWeek']

    def get_KgCO2perYear(self, sorted: bool = False):
        if sorted: 
            return self.df['KgCO2perYear'].sort_values(ascending=False)
        return self.df['KgCO2perYear']
    
    def get_ranking(self, week):
        series:pd.Series = self.get_KgCO2perWeek()
        series.loc["Your Footprint"] = week
        series = series.sort_values(ascending=False)
        user_index = series.index.get_loc("Your Footprint")
        start_index = max(0, user_index - 3)
        end_index = min(len(series), user_index + 4)
        self.ranking = series.iloc[start_index:end_index]
        self.percentage = (210-user_index) / 210
        return self.ranking
    
    def get_percentage(self):
        if self.percentage:
            return self.percentage


def main():
    data_processor = DataProcessor(LOCATION)
    df = data_processor.get_KgCO2perWeek()
    series = data_processor.get_ranking(23.4)
    print(series)
if __name__ == "__main__":
    main()
