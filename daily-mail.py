from email.mime import text
import pandas as pd
from pymongo import TEXT, MongoClient
from decouple import config
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


# MongoDB Auth & Connection
client = MongoClient(config('MONGODB_URI'))

# Connect to specific DB
db = client[config('MONGODB_CLUSTER')]

# Connect to specific Collection
twitter_data = db.twitter
#news_data = db.news

# QUERY FOR CHECKING NEW ITEMS (DAILY REPORT)
query_mail = twitter_data.find({
    "IsMailSent": {"$eq":"false"},
    "Label":{"$ne":"NotRelevant"}
    })
mail_data = []
for i in query_mail:
    mail_data.append({
            'Was': str(i['Label']),
            'Wann': i['Datum'],
            'Zur News': "https://twitter.com/i/web/status/" + str(i['Tweet-Id']),
            'News-Inhalt': i['Tweet']
        }
    )

mail_data = pd.DataFrame(mail_data).sort_values(by=['Wann'], ascending=False)
# print(mail_data)

### IF STATEMENTS & QUERY FUNCTIONS

query_MA = 'MATransaktion'
query_GF = 'WechselGF'

def search_function (element):
    search_df = mail_data[mail_data['Was'].str.contains(element)]
    return search_df

if search_function(query_MA).shape[0] != 0:
    NEWS_info = search_function(query_MA).iloc[0]['News-Inhalt']
    NEWS_date = search_function(query_MA).iloc[0]['Wann']
    NEWS_src =search_function(query_MA).iloc[0]['Zur News']
    MA_head = "Veränderung im Unternehmensbereich"

if search_function(query_GF).shape[0] != 0:
    NEWS_info = search_function(query_GF).iloc[0]['News-Inhalt']
    NEWS_date = search_function(query_GF).iloc[0]['Wann']
    NEWS_src =search_function(query_GF).iloc[0]['Zur News']
    GF_head = "Veränderung in der Unternehmensführung"


    

######### MAIL SETUP

username = config('GMAIL_USER')
password = config('GMAIL_PASSWORD')
msg = EmailMessage()
msg['From'] = username
msg['To'] = ['jannis.holthusen@upchain.io']
msg['Subject'] = 'Dein Daily Report'

class Main:
    MAIL_TO = 'Jannis'
    KUNDE = 'BPD Immobilienentwicklung GmbH'
    INHALT = NEWS_info
    DATUM = NEWS_date
    QUELLE = NEWS_src
    #MATransaktion = MA_head
    GF_WECHSEL = GF_head

HTML_File = open('index.html', 'r')
s =HTML_File.read().format(p=Main())

msg.set_content(s, subtype='html')


try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(username,password)
        connection.send_message(msg)
        connection.quit()
        print("Email erfolgreich versendet :-)")


except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
