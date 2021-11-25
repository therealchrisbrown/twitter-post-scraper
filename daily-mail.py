from email.mime import text
import pymongo
import pandas as pd
from pymongo import TEXT, MongoClient
from decouple import config
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage


# MongoDB Auth & Connection
client = MongoClient(config('mongodb_uri'))

# Connect to specific DB
db = client[config('mongodb_cluster')]

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
            'Was': i['Label'],
            'Wann': i['Datum']
        }
    )

mail_data = pd.DataFrame(mail_data).sort_values(by=['Wann'], ascending=False)
print(mail_data)


######### MAIL SETUP

username = config('gmail_user')
password = config('gmail_password')
msg = EmailMessage()
msg['From'] = username
msg['To'] = ['jannis.holthusen@upchain.io']
msg['Subject'] = 'BPD Immobilien neue Aktion für dich'

class Main:
    KUNDE = 'BPD'
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
