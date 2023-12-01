from scraper import scraper
from mail import mail
from db import db

# read mailing list
def subscribers():
    db.cur.execute('SELECT * FROM subscribers')
    return db.cur.fetchall()

# iterate over subscriptions
def sendNotifications(subscribers):
    for email, number, daily in subscribers:
        # get winning status
        result = scraper.scrape(number)
        if result or int(daily):
            # send email
            mail.notify(email, number, result)

def main():
    sendNotifications(subscribers())

if __name__ == '__main__':
    main()