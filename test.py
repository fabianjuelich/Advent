import unittest
from backend.server import server
from backend.cronjob import main
import threading
import xmlrpc.client

class Test(unittest.TestCase):
    ser: threading.Thread
    # backend
    def setup(self):
        self.ser = threading.Thread(target=server.serve)
        self.ser.start()

    # frontend
    def test_1_web_service(self):
        ser = xmlrpc.client.ServerProxy('http://localhost:2412')
        subscribers = (('omas.adventskalender@gmail.com', 1, False),
                       ('omas.adventskalender@gmail.com', 2, True))
        for subscriber in subscribers:
            self.assertEqual(ser.subscribe(*subscriber) == f'{subscriber[0]} subscribed to {subscriber[2]}')

    # backend
    def test_2_cronjob(self):
        main.main()

    def tearDown(self):
        # self.ser.join()
        pass