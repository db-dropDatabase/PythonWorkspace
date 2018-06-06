import pandas as pd
import datetime

CITIES = ["Las Vegas", "Charlotte", "Pittsburgh", "Toronto"]
DATE_LOWER = datetime.datetime.strptime("2012-10-01 13:00:00", "%Y-%m-%d %H:%M:%S")
DATE_UPPER = datetime.datetime.strptime("2017-11-30 00:00:00", "%Y-%m-%d %H:%M:%S")

review = pd.read_csv("./processed/yelp_review.csv", parse_dates=["date"], infer_datetime_format=True, index_col=0)

for city in CITIES:
    busy_id = pd.read_csv("./processed/buisness/" + city + ".csv", usecols=["business_id"])["business_id"]
    review[(review["date"] >= DATE_LOWER) & (review["date"] <= (DATE_UPPER - pd.DateOffset(hours=12))) & review["business_id"].isin(busy_id)].reset_index(drop=True).to_csv("./processed/review/" + city + ".csv")