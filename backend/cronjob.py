import os, csv
from backend.scraper import scraper
from backend.mail import mail

# read mailing list
def read():
    with open(os.path.join(os.path.dirname(__file__), './data/subscriptions.csv'), 'r') as subs:
        subscriptions = csv.reader(subs.readlines(), delimiter=',')
    return subscriptions

# iterate over subscriptions
def iterate(subscriptions):
    # skip header
    next(subscriptions)
    for email, number, daily in subscriptions:
        # get status
        result = scraper.scrape(number)
        if result or not int(daily):
            # send email
            mail.notify(email, number, result)

def main():
    iterate(read())

if __name__ == '__main__':
    main()