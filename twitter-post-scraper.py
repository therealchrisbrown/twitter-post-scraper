from math import e
from decouple import config
import tweepy as tw
from tweepy import user
import pandas as pd
import time, os, fnmatch, shutil
import csv


auth = tw.OAuthHandler(config('consumer_key'),config('consumer_secret'))
auth.set_access_token(config('access_token'),config('access_secret'))
api = tw.API(auth,wait_on_rate_limit=True)

username = config('twitter_user')
count = 150

try:
    tweets = tw.Cursor(api.user_timeline, id=username).items(count)
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    tweets_list_header = ['Datum', 'Tweet-Id', 'Tweet']
    tweets_df = pd.DataFrame(tweets_list, columns=tweets_list_header).sort_values(['Datum'])

except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
    
existing_tw_data = pd.read_csv('./results/BDPTwitter.csv', error_bad_lines=False, sep=";")

last_date_current = pd.to_datetime(tweets_df['Datum']).iloc[-1]
last_date_existing = pd.to_datetime(existing_tw_data['Datum']).iloc[-1]


if last_date_current == last_date_existing:
    print('Keine neuen Tweets')
else:
    new_tweets = tweets_df.loc[lambda tweets_df: tweets_df['Datum'] > last_date_existing]
    conc_df = new_tweets.to_csv('./results/BDPTwitter.csv', mode='a', header=False, index=False, sep=';')

    print("Es wurden Tweets hinzugefügt")
