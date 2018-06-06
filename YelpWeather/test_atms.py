import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import scatter_matrix

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]

for city in CITIES:
    reviews = pd.read_csv("./processed/weatheratm/" + city + ".csv", nrows=100, usecols=["stars", "mean"])
    reviews.plot.scatter(x="stars", y="mean")
    scatter_matrix(reviews, alpha=0.2, figsize=(6, 6), diagonal='kde')
    plt.show()
