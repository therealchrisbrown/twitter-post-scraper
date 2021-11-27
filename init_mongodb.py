from pymongo import MongoClient
from decouple import config
import pandas as pd


# Connect mongoDB
cluster = MongoClient("mongodb+srv://cbscraper:" + config('mongodb_pw') +"@cluster0.qet17.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster ["scraperDB"]
collection_news = db["news"]
collection_twitter = db["twitter"]

# Data Twitter
TWITTER_RESULTS_PATH = r"/Users/christianbraun/Google Drive/Microserv_scraper/py_twitter-posts-scraper/results/BDPTwitter.csv"
data_twitter = pd.read_csv(TWITTER_RESULTS_PATH, error_bad_lines=False, sep=';')
data_twitter["Company"] = "BPD Immobilienentwicklung"
data_twitter["Label"] = ""

#data_twitter.reset_index(inplace=True)
data_twitter_dict = data_twitter.to_dict('records')

# Post Data to mongoDB
collection_twitter.insert_many(data_twitter_dict)

#print(data_twitter_dict)