import pandas as pd
import numpy as np
import itertools

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]
WEATHER_TYPES = ["cloud", "clear", "rain", "fog", "snow", "storm"]
Z_CRIT = 2.3263

for city in CITIES:
    COMBOS = itertools.product(WEATHER_TYPES, range(1, 6))
    reviews = pd.read_csv("./processed/weather/" + city + ".csv", usecols=["weather", "stars"])
    starCounts = reviews["stars"].value_counts()
    weatherCounts = reviews["weather"].value_counts()
    starWeatherCounts = {weather : reviews[reviews["weather"].str.match(weather)]["stars"].value_counts() for weather in WEATHER_TYPES}
    total = reviews.shape[0]
    storeDict = {"weather" : [], "star" : [], "pd" : [], "se" : []}
    print(city + ": ")
    for weather, star in COMBOS:
        if city == "Las Vegas" and weather == "snow":
            # no snow in vegas baby
            continue
        # get needed numbers
        starTotal = starCounts[star]
        weatherTotal = weatherCounts[weather]
        starWeatherTotal = starWeatherCounts[weather][star]
        # calculate p values
        p1 = starTotal / total
        p2 = starWeatherTotal / weatherTotal
        pc = (starTotal + starWeatherTotal) / (total + weatherTotal)
        # and then standard error
        se = np.sqrt(pc*(1 - pc)*(1/total + 1/weatherTotal))
        # and finally, our p-value and confidence interval
        z = (p1 - p2)/se
        cInd = ((p1 - p2) - Z_CRIT*se, (p1 - p2) + Z_CRIT*se)
        storeDict["weather"].append(weather)
        storeDict["star"].append(star)
        storeDict["pd"].append(p1 - p2)
        storeDict["se"].append(se)
        if np.abs(p1 - p2) > 0.01 and cInd[0] * cInd[1] >= 0: 
            print(weather + ", " + str(star))
            print(z)
            print(cInd)
    pd.DataFrame(storeDict).to_csv("./processed/2prop/" + city + ".csv")


    