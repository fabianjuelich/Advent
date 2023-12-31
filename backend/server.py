import xmlrpc.server, logging, os
from mail import mail
from db import db

# log
logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), './logs/server.log'),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info(__file__)

def initialize():
    db.cur.execute('''CREATE TABLE IF NOT EXISTS subscribers (
            email TEXT NOT NULL,
            number INTEGER NOT NULL,
            daily BOOLEAN NOT NULL,
            PRIMARY KEY (email, number)
    )''')

class Server:

    def subscribe(self, email, number, daily):
        # add to mailing list
        try:
            with db.conn:
                db.cur.execute('INSERT OR REPLACE INTO subscribers VALUES (:email, :number, :daily)', {'email':email, 'number':number, 'daily':daily})
            db.cur.execute('SELECT changes()')
            success = bool(db.cur.fetchone()[0])
        except Exception as e:
            success = False
            logging.error(e)
        if success:
            try:
                mail.subscribed(email, number, daily)
            except Exception as e:
                logging.error(e)
        return success
    
    def unsubscribe(self, email, number):
        # remove from mailing list
        try:
            with db.conn:
                db.cur.execute('DELETE FROM subscribers WHERE email = :email AND number = :number', {'email':email, 'number':number})
            db.cur.execute('SELECT changes()')
            success = bool(db.cur.fetchone()[0])
        except Exception as e:
            success = False
            logging.error(e)
        if success:
            try:
                mail.unsubscribed(email, number)
            except Exception as e:
                logging.error(e)
        return success

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 2413))
    server.register_instance(Server())
    server.serve_forever()

def main():
    initialize()
    serve()

if __name__ == "__main__":
    main()