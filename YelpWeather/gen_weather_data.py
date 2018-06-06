import pandas as pd

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]

WEATHER_FOLD = {
    "cloud" : [
        "overcast clouds",
        "broken clouds",
        "scattered clouds",
        "few clouds",
    ],
    "clear" : [
        "sky is clear",
    ],
    "rain" : [
        "light rain",
        "moderate rain",
        "light intensity shower rain",
        "heavy intensity rain",
        "proximity shower rain",
        "light intensity drizzle",
        "very heavy rain",
        "shower rain",
        "heavy intensity shower rain",
        "drizzle",
        "light intensity drizzle rain",
        "heavy intensity drizzle",
        "proximity thunderstorm with rain",
    ],
    "fog" : [
        "mist",
        "haze",
        "fog",
        "dust",
        "smoke",
    ],
    "snow" : [
        "light snow",
        "light shower snow",
        "heavy snow",
        "snow",
        "heavy shower snow",
        "light shower sleet",
        "shower snow",
        "freezing rain",
        "light rain and snow",
        "rain and snow",
    ],
    "storm" : [
        "thunderstorm with light rain",
        "proximity thunderstorm",
        "thunderstorm",
        "thunderstorm with rain",
        "thunderstorm with heavy rain",
        "squalls",
        "thunderstorm with drizzle",
    ]
}

weather = pd.read_csv("./historical-hourly-weather-data/weather_description.csv", index_col=0,
    parse_dates=True, infer_datetime_format=True, usecols=CITIES + ["datetime"])



for city in CITIES:
    print(pd.value_counts(weather[city]))
    for category, matches in WEATHER_FOLD.items():
        weather[city].replace(to_replace=matches, value=category, inplace=True)
    print(pd.value_counts(weather[city]))

weather.to_csv("./processed/weather_catigorical.csv")

