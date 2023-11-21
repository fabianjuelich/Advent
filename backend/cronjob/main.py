import os, csv
from backend.cronjob.scraper import scrape
from backend.cronjob.mail import notify

# read mailing list
def read():
    with open(os.path.join(os.path.dirname(__file__), '../data/subscriptions.csv'), 'r') as s:
        subscriptions = csv.reader(s.readlines(), delimiter=',')
    return subscriptions

# iterate over subscriptions
def iterate(subscriptions):
    # skip header
    next(subscriptions)
    for email, number, onlyOnWin in subscriptions:
        # get status
        result = scrape(number)
        if result or not onlyOnWin:
            # send email
            notify(email, number, result)

def main():
    iterate(read())

if __name__ == '__main__':
    main()