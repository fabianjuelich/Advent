from scraper import scraper
from mail import mail
from db import db
import logging, os

# log
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), './logs/cronjob.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info(__file__)

# read mailing list
def subscribers():
    db.cur.execute('SELECT * FROM subscribers')
    return db.cur.fetchall()

# iterate over subscriptions
def sendNotifications(subscribers):
    scrape = scraper.Scraper()
    for email, number, daily in subscribers:
        # get winning status
        try:
            result = scrape.result(number)
            if result or int(daily):
                # send email
                mail.notify(email, number, result)
        except Exception as e:
            logging.error(e)

def main():
    sendNotifications(subscribers())

if __name__ == '__main__':
    main()