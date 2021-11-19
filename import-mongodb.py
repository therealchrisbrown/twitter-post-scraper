import pymongo
import pandas as pd
from pymongo import MongoClient
from decouple import config

# MongoDB Auth & Connection
client = MongoClient(config('mongodb_uri'))

# Connect to specific DB
db = client[config('mongodb_cluster')]

# Connect to specific Collection
twitter_data = db.twitter
news_data = db.news

#news_data.insert({"_id": 1, "name": "chriz", "score": 2})

# Dataframe
twitter_data = pd.DataFrame(list(twitter_data.find()))

print(twitter_data)