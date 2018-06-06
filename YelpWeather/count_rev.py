import pandas as pd
import matplotlib.pyplot as plt

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]

reviews = pd.read_csv("./processed/weather/Charlotte.csv", usecols=["weather", "stars"])

counts = reviews["stars"].value_counts().sort_index()
stormCounts = reviews[reviews["weather"].str.match("snow")]["stars"].value_counts().sort_index()

df = pd.DataFrame({"Overall" : counts / sum(counts), "Snow" : stormCounts / sum(stormCounts) })

axes = df.plot(kind="bar", title="Charlotte Proportional Distribution Of Star Rating")
axes.set_xlabel("Star Rating")
axes.set_ylabel("Proportion")
plt.show()
