import os, xmlrpc.server, csv

subs_csv = os.path.join(os.path.dirname(__file__), './data/subscriptions.csv')

def createCsv():
    if not os.path.isfile(subs_csv):
        with open(subs_csv, 'w+') as subs:
            writer = csv.writer(subs)
            writer.writerow(('email', 'number', 'onlyOnWin'))

class Server:
    def subscribe(self, email, number, onlyOnWin):
        # append to mailing list
        with open(subs_csv, 'a') as subs:
            writer = csv.writer(subs)
            writer.writerow((email, number, int(onlyOnWin)))
        # feedback
        return f'{email} subscribed to {number} ({onlyOnWin})'

def serve():
    server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 2413))
    server.register_instance(Server())
    server.serve_forever()

def main():
    createCsv()
    serve()

if __name__ == "__main__":
    main()