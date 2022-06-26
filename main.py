import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
now = datetime.datetime.now()

content = ''

def extract_news(url):
    print ('Getting ready news headlines')
    cnt = ''
    cnt += ('<b> HN TOP STORIES:</B>\n'+'<br>'+'-'*50+'<br> ')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td', attrs={'class' : 'title', 'valign': ''})):
        cnt += ((str(i+1)+' :: '+tag.text + "\n" + '<br>') if tag.text != 'More' else '')
    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br>End of Message')

print('composing Email...')

#AUTHENTICATION
SERVER = 'smtp.gmail.com'
PORT = 465
FROM = 'adoghedaniel@gmail.com'
TO = 'adoghedaniel@gmail.com'
PASS = 'ctlnitdnmgeqttrp'

#EMAIL BODY
msg = MIMEMultipart()
msg['Subject'] = 'TOP HN STORIES FOR Daniel [automated]' + '' + str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['from'] = FROM
msg['to'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initialing server...')

server = smtplib.SMTP_SSL(SERVER, PORT)
server.set_debuglevel(1)
server.ehlo()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()



