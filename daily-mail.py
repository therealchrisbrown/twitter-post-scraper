import pymongo
import pandas as pd
from pymongo import TEXT, MongoClient
from decouple import config
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
gmail_user = config('gmail_user')
gmail_password = config('gmail_password')

# SERVER = "localhost"
message = MIMEMultipart()
FROM = gmail_user
TO = ["christian.braun@upchain.io"]
SUBJECT = 'BPD Immobilien neue Aktion für dich'
mail_content = '''Dies ist eine Testmail. Es gibt folgende Alerts'''
TEXT = 'Bei deinem Kunden BPD Immobilien gibt es folgenden Alert'

message = """\

%s
""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(FROM, TO, message)
    # dev_server = smtplib.SMTP('localhost', 1025)
    # dev_server.sendmail(FROM,TO,message)

    print("Email erfolgreich versendet :-)")
except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
else:
    print("Keine neue Mail versendet")



# if twitter_data.count_documents({"IsMailSent":"false"}, limit = 1) != 0:
 
#     label_data = pd.DataFrame(list(twitter_data.find_one()))