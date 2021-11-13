from math import e
from decouple import config
import tweepy as tw
from tweepy import user
import pandas as pd
import time, os, fnmatch, shutil


auth = tw.OAuthHandler(config('consumer_key'),config('consumer_secret'))
auth.set_access_token(config('access_token'),config('access_secret'))
api = tw.API(auth,wait_on_rate_limit=True)

username = config('twitter_user')
count = 150

try:
    tweets = tw.Cursor(api.user_timeline, id=username).items(count)
    tweets_list = [[tweet.created_at, tweet.id, tweet.text] for tweet in tweets]
    tweets_df = pd.DataFrame(tweets_list)

except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)

#print(tweets_df)
t = time.localtime()
timestamp = time.strftime('%Y%m%d',t)
FILE_NAME = (timestamp + "_BDPTwitter.csv")
tweets_df.to_csv('./results/' + FILE_NAME,index=False, sep=';')