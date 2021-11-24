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
#mail_from = username
msg['From'] = username
#mail_to = ['christian.braun@upchain.io','ch.braun02@gmail.com']
msg['To'] = ['jannis.holthusen@upchain.io']
msg['Subject'] = 'BPD Immobilien neue Aktion für dich'

class Main:
    KUNDE = 'Jannis Firma'
HTML_File = open('index.html', 'r')
s =HTML_File.read().format(p=Main())

msg.set_content(s, subtype='html')


# <!DOCTYPE html>
# <html>
#     <body>
#         <div style="background-color:#eee;padding:10px 20px;">
#             <h2 style="font-family:Open Sans, 'Times New Roman', Times, serif;color#454349;">Daily Report</h2>
#         </div>
#         <div style="padding:20px 0px">
#             <div style="height: 500px;width:400px">
#                 <div style="text-align:left;">
#                     <h3>Kunde: </h3>
#                     <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. A ducimus deleniti nemo quibusdam iste sint!</p>
#                     <a href="#">Read more</a>
#                 </div>
#             </div>
#         </div>
#     </body>
# </html>

#mail_subject = 'BPD Immobilien neue Aktion für dich'
#mail_body = ""

# html = """\
# <html>
#   <head>Für deinen Kunden 'BPD Immobilien' gibt folgende Alerts</head>
#   <body>
#     {0}
#   </body>
# </html>
# """.format(mail_data.to_html())

# part1 = MIMEText(html, 'html')
# mimemsg = MIMEMultipart()
# # mimemsg['From']=mail_from
# # mimemsg['To']=mail_to
# # mimemsg['Subject']=mail_subject
# mimemsg.attach(part1)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:
        connection.login(username,password)
        connection.send_message(msg)
        connection.quit()
        print("Email erfolgreich versendet :-)")


except BaseException as e:
    print('failed on_status,',str(e))
    time.sleep(3)
# else:
#     print("Keine neue Mail versendet")



# SERVER = "localhost"
# message = MIMEMultipart()
# FROM = gmail_user
# TO = []
# message['From'] = FROM
# message['To'] = TO
# message['Subject'] = 
# mail_content = ''''''
# message.attach(MIMEText(mail_content, 'plain'))

# TEXT = 'Bei deinem Kunden BPD Immobilien gibt es folgenden Alert'

# message = """\

# %s
# """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

# try:
#     server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#     #server.starttls()
#     server.ehlo()
#     server.login(gmail_user, gmail_password)
#     text = message.as_string()
#     server.sendmail(FROM, TO, text)
#     # dev_server = smtplib.SMTP('localhost', 1025)
#     # dev_server.sendmail(FROM,TO,message)

#     print("Email erfolgreich versendet :-)")
# except BaseException as e:
#     print('failed on_status,',str(e))
#     time.sleep(3)
# else:
#     print("Keine neue Mail versendet")



# if twitter_data.count_documents({"IsMailSent":"false"}, limit = 1) != 0:
 
#     label_data = pd.DataFrame(list(twitter_data.find_one()))