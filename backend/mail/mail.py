import os, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from mail import credentials

# text fields #
day = datetime.datetime.today().strftime("%d. %B")
# lost
subject_lose = '📅 Hinter diesem Türchen war leider nichts'
quote = 'Wer nicht verlieren kann, verdient auch nicht zu gewinnen.'
# won
subject_win = '🎁 Hinter diesem Türchen war ein Gewinn'
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
    subject = f"({number}) ✅ Bestätigung von Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender"
    fallback = (subscribedPlain.format(number=number, daily='täglich ' if daily else ''))
    confirmation = (subscribedHTML.format(number=number, daily='täglich ' if daily else ''))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), confirmation, fallback)
    mail.send()

def unsubscribed(email: str, number: int):
    # fill placeholders
    subject = f"({number}) ✅ Abbestellung von Benachrichtigungsabo für Lions-Club-Adventsgewinnkalender"
    fallback = (unsubscribedPlain.format(number=number))
    confirmation = (unsubscribedHTML.format(number=number))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), confirmation, fallback)
    mail.send()

# send notification
def notify(email: str, number: int, win):
    # fill placeholders
    subject = f"({number}) {subject_win if win else subject_lose}"
    fallback = (notificationPlain.format(number=number, day=day, statement=congrats.format(win=win) if win else quote))
    notification = (notificationHTML.format(number=number, day=day, statement=congrats.format(win=win) if win else f'<q>{quote}</q>'))
    # send
    mail = Mail(subject, (credentials.realname, credentials.email_user), (str(number), email), notification, fallback)
    mail.send()