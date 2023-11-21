import unittest, threading, xmlrpc.client, os
from backend.server import server
from backend.cronjob import main
from backend.data import credentials

class Test(unittest.TestCase):
    ser: threading.Thread
    # backend
    @classmethod
    def setupClass(self):
        # self.ser = threading.Thread(target=server.serve)
        # self.ser.start()
        pass    # start manually

    # frontend
    def test_1_web_service(self):
        ser = xmlrpc.client.ServerProxy('http://localhost:2412')
        subscribers = ((credentials.email_user, 1, False),  # False: mail -> lose   True: mail -> win
                       (credentials.email_user, 2, True))   # False: no mail        True: mail -> win
        for subscriber in subscribers:
            self.assertEqual(ser.subscribe(*subscriber), f'{subscriber[0]} subscribed to {subscriber[1]} ({subscriber[2]})')

    # backend
    def test_2_cronjob(self):
        main.main()

    @classmethod
    def tearDownClass(self):
        with open(os.path.join(os.path.dirname(__file__), 'backend/data/subscriptions.csv'), 'w') as subs:
            subs.write('email,number,onlyOnWin\n')