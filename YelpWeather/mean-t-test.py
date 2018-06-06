import pandas as pd
import numpy as np
import itertools

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]
WEATHER_TYPES = ["cloud", "clear", "rain", "fog", "snow", "storm"]
Z_CRIT = 2.3263

for city in ["Las Vegas"]:
    reviews = pd.read_csv("./processed/weather/" + city + ".csv", usecols=["weather", "stars"])
    total = reviews.shape[0]
    starCounts = reviews["stars"].value_counts() 
    starMean = sum([starCounts[x] * x for x in range(1, 6)]) / total
    starSx2 = sum([starCounts[x]*np.power(x - starMean, 2) for x in range(1, 6)])/(total - 1)
    starWeatherCounts = {weather : reviews[reviews["weather"].str.match(weather)]["stars"].value_counts() for weather in WEATHER_TYPES}
    storeDict = {"weather" : [], "md" : [], "se" : []}
    print(city + ": ")
    for weather in WEATHER_TYPES:
        if city == "Las Vegas" and weather == "snow":
            # no snow in vegas baby
            continue
        # find conditional weather mean
        starWeatherTotal = sum(starWeatherCounts[weather])
        starWeatherMean = sum([starWeatherCounts[weather][x] * x for x in range(1, 6)]) / starWeatherTotal
        starWeatherSx2 = sum([starWeatherCounts[weather][x]*np.power(x - starWeatherMean, 2) for x in range(1, 6)])/(starWeatherTotal - 1)
        # calc
        se = np.sqrt(starSx2/total + starWeatherSx2/starWeatherTotal)
        t = (starMean - starWeatherMean)/se
        print(weather)
        print(starMean - starWeatherMean)
        print(t)
        storeDict["weather"].append(weather)
        storeDict["md"].append(starMean - starWeatherMean)
        storeDict["se"].append(se)
        if weather == "storm":
            pass
    pd.DataFrame(storeDict).to_csv("./processed/2mean/" + city + ".csv")
