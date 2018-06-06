import pandas as pd
from scipy import stats

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]
NROWS = 50

weather = pd.read_csv("./processed/weather_catigorical.csv", index_col=0,
    parse_dates=["datetime"], infer_datetime_format=True)

for city in CITIES:
    reviews = pd.read_csv("./processed/review/" + city + ".csv", usecols=["business_id", "stars", "date"], 
        parse_dates=["date"], infer_datetime_format=True)
    
    # get all the weather for the given day form 9-9
    start = reviews["date"] + pd.DateOffset(hours=9)

    def get_dominant_weather(date):
        global weather
        global city
        return weather[date : date + pd.DateOffset(hours=12)][city].value_counts().idxmax()

    reviews["weather"] = start.apply(get_dominant_weather)

    reviews.to_csv("./processed/weather/" + city + ".csv")

    print(city + ": ")
    print(stats.chi2_contingency(pd.crosstab(reviews["stars"], reviews["weather"])))


    

