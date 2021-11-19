from math import e
from decouple import config
import tweepy as tw
from tweepy import user
import pandas as pd
import time, os, fnmatch, shutil
import csv
import pymongo
from pymongo import MongoClient
import datetime

### COMPANY
COMPANY = config('COMPANY_NAME')

# Connect mongoDB
client = MongoClient(config('mongodb_uri'))
db = client[config('mongodb_cluster')]
collection_twitter = db["twitter"]

# Twitter Auth & Config
auth = tw.OAuthHandler(config('consumer_key'),config('consumer_secret'))
auth.set_access_token(config('access_token'),config('access_secret'))
api = tw.API(auth,wait_on_rate_limit=True)
username = config('twitter_user')
count = 150

### DATA
try:
    tweets = tw.Cursor(api.user_timeline, id=username).items(count)
    tweets_list = []
    for tweet in tweets:
        created_at = tweet.created_at 
        created_at = str(created_at)
        tweet_dt = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S+00:00')
        tweets_list.append(
            {
                'Datum': created_at,
                'Tweet-Id': tweet.id,
                'Tweet': tweet.text,
                'Company': COMPANY,
                'Source': "Twitter",
                'Label': ""
            }
        )
    tweets_df = pd.DataFrame(tweets_list).sort_values(by=['Datum'], ascending=True)

except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
    
#existing_tw_data = pd.read_csv('./results/BDPTwitter.csv', error_bad_lines=False, sep=";")
existing_tw_data = pd.DataFrame(list(collection_twitter.find()))

last_date_current = pd.to_datetime(tweets_df['Datum']).iloc[-1]
last_date_existing = pd.to_datetime(existing_tw_data['Datum']).iloc[-1]

### ERGEBNIS
if last_date_current == last_date_existing:
    print("#### Keine neuen Tweets ####")

else:
    new_tweets = tweets_df.loc[lambda tweets_df: pd.to_datetime(tweets_df['Datum']) > last_date_existing]
    #conc_df = new_tweets.to_csv('./results/BDPTwitter.csv', mode='a', header=False, index=False, sep=';')

    new_data_mdb_dict = new_tweets.to_dict('records')
    collection_twitter.insert_many(new_data_mdb_dict)

    print("#### Es wurden Tweets hinzugefügt ####")