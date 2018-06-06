import pandas as pd
import scipy.stats as stats
import numpy as np

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]
NROWS = 10

atms = pd.read_csv("./historical-hourly-weather-data/pressure.csv", usecols=CITIES + ["datetime"], 
    index_col=0, parse_dates=["datetime"], infer_datetime_format=True)

for city in CITIES:
    reviews = pd.read_csv("./processed/review/" + city + ".csv", usecols=["business_id", "stars", "date"],
        parse_dates=["date"], infer_datetime_format=True)

    dated = reviews["date"] + pd.DateOffset(hours=9)

    atmsRow = atms[city]
    # calculate statistics columns (row level)
    def calcStats(date, atmsRow=None):
        atmSet = atmsRow[date : date + pd.DateOffset(hours=12)]
        result = stats.describe(atmSet.values, nan_policy="omit")
        meds = np.nanpercentile(atmSet.values, [25, 50, 75], interpolation="nearest")
        mode = stats.mode(atmSet.values)
        return pd.Series([result.nobs, result.minmax[0], result.minmax[1], result.mean, result.variance, result.skewness, result.kurtosis, meds[0], meds[1], meds[2], mode.mode[0]],
            index=["nobs", "min", "max", "mean", "variance", "skewness", "kurtosis", "q1", "median", "q3", "mode"])
    # calculate statistics columns (dataframe level)
    def addStats(datedf, atmsRow):
        return datedf.apply(calcStats, atmsRow=atmsRow)
    
    print(city)
    pd.concat([reviews, addStats(dated, atmsRow)], axis=1).to_csv("./processed/weatheratm/" + city + ".csv")