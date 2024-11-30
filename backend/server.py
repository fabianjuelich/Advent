import xmlrpc.server, logging, os
from mail import mail
from db import db
from enum import Enum

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

class Subscription(Enum):
    CREATED = 0
    UPTODATE = 1
    UPDATED = 2
    ERROR = 3
    EXCEPTION = 4

USER_LIMIT = 100

class Server:
    def subscribe(self, email, number, daily):
        # add to mailing list
        try:
            with db.conn:
                # check if the record already exists
                db.cur.execute('SELECT * FROM subscribers WHERE email = :email AND number = :number', {'email':email, 'number':number})
                record = db.cur.fetchone()
                if record:
                # record exists
                    if daily == record[2]:
                    # is the same
                        result = Subscription.UPTODATE
                    else:
                    # needs to be updated
                        db.cur.execute('UPDATE subscribers SET daily = :daily WHERE email = :email AND number = :number', { 'daily':daily, 'email':email, 'number':number})
                        if db.changes_made():
                            result = Subscription.UPDATED
                            mail.subscribed(email, number, daily, True)
                        else:
                            result = Subscription.ERROR
                else:
                # record does not exist
                    # check if the subscriber limit has been reached
                    db.cur.execute("SELECT COUNT(*) FROM subscribers")
                    row_count = db.cur.fetchone()[0]
                    if row_count < USER_LIMIT:
                        db.cur.execute('INSERT OR REPLACE INTO subscribers VALUES (:email, :number, :daily)', {'email':email, 'number':number, 'daily':daily})
                        if db.changes_made():
                            result = Subscription.CREATED
                            mail.subscribed(email, number, daily, False)
                        else:
                            result = Subscription.ERROR
                    else:
                        result = Subscription.ERROR

        except Exception as e:
            result = Subscription.EXCEPTION
            logging.error(e)
        return result.value
    
    def unsubscribe(self, email, number):
        # remove from mailing list
        try:
            with db.conn:
                db.cur.execute('DELETE FROM subscribers WHERE email = :email AND number = :number', {'email':email, 'number':number})
            success = db.changes_made()
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
