import os, smtplib, datetime, locale, math
from enum import StrEnum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from mail import credentials

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

class Advent(StrEnum):
    FIRST = '1. Advent'
    SECOND = '2. Advent'
    THIRD = '3. Advent'
    FOURTH = '4. Advent'
    CHRISTMAS = 'Heiligabend'

def checkAdvent(date):
    if int(date.strftime('%d')) == 24 and int(date.strftime('%m')) == 12:
        return Advent.CHRISTMAS
    if date.strftime('%a') == 'So' and int(date.strftime('%d')) in range(1,25) and int(date.strftime('%m')) == 12:
        return 'der ' + list(Advent)[math.ceil(int(date.strftime('%d')) / 7) - 1].value
    return 'der ' + date.strftime('%-d. %B')

# text fields #
num = '({number})'
day = checkAdvent(datetime.datetime.today())
# subscription
subject_subscribed = num + ' 🔔 Bestätigung von Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender'
subject_unsubscribed = num + ' 🔕 Abbestellung von Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender'
# lost
subject_lose = num + ' 📅 Hinter diesem Türchen war leider nichts'
quote = 'Wer nicht verlieren kann, verdient auch nicht zu gewinnen.'
# won
subject_win = num + ' 🎁 Hinter diesem Türchen war ein Gewinn'
congrats = "Du hast '{win}' gewonnen."

# read content
with open(os.path.join(os.path.dirname(__file__), './notification.txt'), 'r') as noteP, \
    open(os.path.join(os.path.dirname(__file__), './notification.html'), 'r') as noteH, \
    open(os.path.join(os.path.dirname(__file__), './subscribed.txt'), 'r') as subP, \
    open(os.path.join(os.path.dirname(__file__), './subscribed.html'), 'r') as subH, \
    open(os.path.join(os.path.dirname(__file__), './unsubscribed.txt'), 'r') as unsubP, \
    open(os.path.join(os.path.dirname(__file__), './unsubscribed.html'), 'r') as unsubH:
    notificationPlain = noteP.read()
    notificationHTML = noteH.read()
    subscribedPlain = subP.read()
    subscribedHTML = subH.read()
    unsubscribedPlain = unsubP.read()
    unsubscribedHTML = unsubH.read()

class Mail():

    def __init__(self, subject, fromAddr, toAddr, html, plain):
        self.toAddr = toAddr
        # create message
        self.msg = MIMEMultipart('alternative')
        self.msg['From'] = formataddr(fromAddr)
        self.msg['To'] = formataddr(toAddr)
        self.msg['Subject'] = subject
        # attach documents to message (order matters)
        self.msg.attach(MIMEText(plain, 'plain'))
        self.msg.attach(MIMEText(html, 'html'))

    def send(self):
        # encrypted communication
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(credentials.email_user, credentials.email_password)
            smtp.sendmail(credentials.email_user, self.toAddr[1], self.msg.as_string())

# send confirmation
def subscribed(email: str, number: int, daily: bool):
    # fill placeholders
    subject = subject_subscribed.format(number=number)
    fallback = (subscribedPlain.format(number=number, daily='täglich ' if daily else ''))
    confirmation = (subscribedHTML.format(number=number, daily='täglich ' if daily else ''))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), confirmation, fallback)
    mail.send()

def unsubscribed(email: str, number: int):
    # fill placeholders
    subject = subject_unsubscribed.format(number=number)
    fallback = (unsubscribedPlain.format(number=number))
    confirmation = (unsubscribedHTML.format(number=number))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), confirmation, fallback)
    mail.send()

# send notification
def notify(email: str, number: int, win):
    # fill placeholders
    subject = (subject_win if win else subject_lose).format(number=number)
    fallback = (notificationPlain.format(number=number, day=day, statement=congrats.format(win=win) if win else quote))
    notification = (notificationHTML.format(number=number, day=day, statement=congrats.format(win=win) if win else f'<q>{quote}</q>'))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), notification, fallback)
    mail.send()