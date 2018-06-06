import pandas as pd

CITIES = ["las vegas", "charlotte", "pittsburgh", "toronto", "montreal", "dallas"]

busy = pd.read_csv("yelp-dataset/yelp_business.csv", usecols=["business_id", "name", "city", "latitude", "longitude", "stars", "review_count"])
for city in CITIES:
    busy[busy["city"].str.lower().str.contains(city, na=False)].drop("city", axis=1).reset_index(drop=True).to_csv("./processed/buisness/" + city + ".csv")