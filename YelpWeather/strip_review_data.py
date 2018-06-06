import pandas as pd

review = pd.read_csv("yelp-dataset/yelp_review.csv")

print(review.head())
review.drop(labels=["text", "useful", "funny", "cool", "user_id"], axis=1, inplace=True)
print(review.head())
review.to_csv("processed/yelp_review.csv")