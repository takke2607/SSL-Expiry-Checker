'''
Command to run the script :

python3 mailsend.py <recipients_list.txt> <file_content_to_be_sent.txt> "<Mail_subject>"

eg: python3 mailsend.py hysecure_dev_team.txt sonarcloud_result.txt
'''

import smtplib , json, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open('mailCreds.json')
data = json.load(f)
username = data['username']
password = data['password']
mail_from = data['username']
with open( sys.argv[1],"r") as ml:
    recipients = [line.strip() for line in ml]
mail_to =  ", ".join(recipients)
with open( sys.argv[2],'r') as file:
    mail_body = file.read()
mimemsg = MIMEMultipart()
mimemsg['From']=mail_from
mimemsg['To']=mail_to
mimemsg['Subject']=sys.argv[3]
mimemsg.attach(MIMEText(mail_body, 'plain'))
connection = smtplib.SMTP(host=data['host'], port=587)
connection.starttls()
connection.login(username,password)
connection.send_message(mimemsg)
connection.quit() 
f.close()
