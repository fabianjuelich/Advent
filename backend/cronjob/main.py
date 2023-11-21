import os, csv
from backend.cronjob.scraper import scrape
from backend.cronjob.mail import notify

# read mailing list
def read():
    with open(os.path.join(os.path.dirname(__file__), '../data/subscriptions.csv'), 'r') as subs:
        subscriptions = csv.reader(subs.readlines(), delimiter=',')
    return subscriptions

# iterate over subscriptions
def iterate(subscriptions):
    # skip header
    next(subscriptions)
    print('iterate')
    for email, number, onlyOnWin in subscriptions:
        # get status
        result = scrape(number)
        if result or not int(onlyOnWin):
            # send email
            notify(email, number, result)

def main():
    iterate(read())

if __name__ == '__main__':
    main()