import sys, os, ssl, smtplib, datetime, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import credentials

quote = 'Wer nicht verlieren kann, verdient auch nicht zu gewinnen.'
congrats = "Du hast '{win}' gewonnen."
subject_won = 'Hinter diesem Türchen war ein Gewinn 🎁'
subject_lost = 'Hinter diesem Türchen war leider nichts 🚪'
day = datetime.datetime.today().day

with open(os.path.join(os.path.dirname(__file__), '../data/subscriptions.csv')) as s,\
open(os.path.join(os.path.dirname(__file__), '../data/content.txt')) as p,\
open(os.path.join(os.path.dirname(__file__), '../data/content.html')) as h:
    subs = s.readlines()
    plain = p.read()
    html = h.read()

subscriptions = csv.reader(subs, delimiter=',')
next(subscriptions)
for email, number, date in subscriptions:
    win = None

    # scrape website
    win = 'Gutschein'
    #

    subject = subject_won if win else subject_lost
    content_plain = (plain.format(number=number, day=day, statement=congrats.format(win=win) if win else quote))
    content_html = (html.format(number=number, day=day, statement=congrats.format(win=win) if win else f'<q>{quote}</q>'))

    msg = MIMEMultipart('alternative')
    msg['From'] = credentials.email_user
    msg['To'] = email
    msg['Subject'] = f"{number}: {subject}"

    content = MIMEText(content_html, 'html')
    fallback = MIMEText(content_plain, 'plain')

    msg.attach(fallback)
    msg.attach(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(credentials.email_user, credentials.email_password)
        smtp.sendmail(credentials.email_user, email, msg.as_string())