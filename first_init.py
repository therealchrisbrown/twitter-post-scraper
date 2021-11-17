    #### USE FOR FIRST RUN ####

from decouple import config
import tweepy as tw
from tweepy import user
import pandas as pd
import time

### COMPANY
COMPANY = config('COMPANY_NAME')

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
    tweets_df["Company"] = COMPANY
    tweets_df["Label"] = ""

    FILE_NAME = ("BDPTwitter.csv")
    tweets_df.to_csv('./results/' + FILE_NAME,index=False, sep=';')

except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)