import sys, os, ssl, smtplib, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data import credentials

# text fields #
day = datetime.datetime.today().day
# lose
subject_lost = 'Hinter diesem Türchen war leider nichts 🚪'
quote = 'Wer nicht verlieren kann, verdient auch nicht zu gewinnen.'
# win
subject_won = 'Hinter diesem Türchen war ein Gewinn 🎁'
congrats = "Du hast '{win}' gewonnen."

# read content
with open(os.path.join(os.path.dirname(__file__), '../data/content.txt')) as p, open(os.path.join(os.path.dirname(__file__), '../data/content.html')) as h:
    plain = p.read()
    html = h.read()

# send notification
def notify(email: str, number: int, win):
    pass

    # fill placeholders
    subject = subject_won if win else subject_lost
    content_plain = (plain.format(number=number, day=day, statement=congrats.format(win=win) if win else quote))
    content_html = (html.format(number=number, day=day, statement=congrats.format(win=win) if win else f'<q>{quote}</q>'))

    # create message
    msg = MIMEMultipart('alternative')
    msg['From'] = formataddr((credentials.realname, credentials.email_user))
    msg['To'] = formataddr((number, email))
    msg['Subject'] = f"({number}) {subject}"

    # create documents
    content = MIMEText(content_html, 'html')
    fallback = MIMEText(content_plain, 'plain')

    # attach documents to message
    msg.attach(fallback)
    msg.attach(content)

    # default settings
    context = ssl.create_default_context()

    # encrypted communication
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(credentials.email_user, credentials.email_password)
        smtp.sendmail(credentials.email_user, email, msg.as_string())