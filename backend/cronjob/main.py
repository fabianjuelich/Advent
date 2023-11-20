import os, csv
from scraper import scrape
from mail import notify

# read mailing list
with open(os.path.join(os.path.dirname(__file__), '../data/subscriptions.csv')) as s:
    subscriptions = csv.reader(s.readlines(), delimiter=',')

# skip header
next(subscriptions)

# iterate over subscriptions
for email, number in subscriptions:

    # send email
    notify(email, number, scrape(number))