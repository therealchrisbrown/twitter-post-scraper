from math import e
from decouple import config
import tweepy as tw
import numpy as np
import pandas as pd
import time
from pymongo import MongoClient
import datetime
import schedule
import os

from flask import Flask

app = Flask(__name__)
@app.route('/')

def home():
    def scraper():
        ### COMPANY
        COMPANY = config('COMPANY_NAME')

        # Connect mongoDB
        client = MongoClient(config('MONGODB_URI'))
        db = client[config('MONGODB_CLUSTER')]
        collection_twitter = db["twitter"]

        # Twitter Auth & Config
        auth = tw.OAuthHandler(config('CONSUMER_KEY'),config('CONSUMER_SECRET'))
        auth.set_access_token(config('ACCESS_TOKEN'),config('ACCESS_SECRET'))
        api = tw.API(auth,wait_on_rate_limit=True)
        username = config('TWITTER_USER')
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
                        'Label': "",
                        'IsMailSent': "false"
                    }
                )
            tweets_df = pd.DataFrame(tweets_list).sort_values(by=['Datum'], ascending=True)

        except BaseException as e:
            print('failed on_status,',str(e))
            time.sleep(3)
            
        ### CHECK NEW DATA & ERGEBNIS
        existing_tw_data = pd.DataFrame(list(collection_twitter.find()))
        last_date_current = pd.to_datetime(tweets_df['Datum']).iloc[-1]
        last_date_existing = pd.to_datetime(existing_tw_data['Datum']).iloc[-1]

        if last_date_current == last_date_existing:
            print("#### Keine neuen Tweets ####")

        else:
            new_tweets = tweets_df.loc[lambda tweets_df: pd.to_datetime(tweets_df['Datum']) > last_date_existing]
            #conc_df = new_tweets.to_csv('./results/BDPTwitter.csv', mode='a', header=False, index=False, sep=';')

            new_data_mdb_dict = new_tweets.to_dict('records')
            collection_twitter.insert_many(new_data_mdb_dict)

            print("#### Es wurden Tweets hinzugef??gt ####")

        return("Script ist gelaufen")
        

    # schedule.every().day.at("08:30").do(scraper)
    schedule.every(30).minutes.do(scraper)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
     app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
