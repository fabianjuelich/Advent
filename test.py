import unittest, threading, xmlrpc.client, os
from backend import server, cronjob
from backend.data import credentials

class Test(unittest.TestCase):
    ser: threading.Thread
    # backend
    @classmethod
    def setupClass(self):
        pass    # started with docker

    # frontend
    def test_1_web_service(self):
        ser = xmlrpc.client.ServerProxy('http://localhost:2413')
        subscribers = ((credentials.email_user, 1, False),  # False: mail -> lose   True: mail -> win
                       (credentials.email_user, 2, True))   # False: no mail        True: mail -> win
        for subscriber in subscribers:
            self.assertEqual(ser.subscribe(*subscriber), f'{subscriber[0]} subscribed to {subscriber[1]} ({subscriber[2]})')

    # backend
    def test_2_cronjob(self):
        cronjob.main()

    @classmethod
    def tearDownClass(self):
        with open(os.path.join(os.path.dirname(__file__), 'backend/data/subscriptions.csv'), 'w') as subs:
            subs.write('email,number,onlyOnWin\n')