import xmlrpc.server
from mail import mail
from db import db

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
            success = True
        except:
            success = False
        if success:
            try:
                mail.subscribed(email, number, daily)
            except Exception as e:
                raise e
        return success
    
    def unsubscribe(self, email, number):
        # remove from mailing list
        try:
            with db.conn:
                db.cur.execute('DELETE FROM subscribers WHERE email = :email AND number = :number', {'email':email, 'number':number})
            success = True
        except:
            success = False
        if success:
            try:
                mail.unsubscribed(email, number)
            except Exception as e:
                raise e
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