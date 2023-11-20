import os, xmlrpc.server, csv

class Server:
    def subscribe(self, email, number):
        # append to mailing list
        with open(os.path.join(os.path.dirname(__file__), '../data/subscriptions.csv'), 'a') as subs:
            writer = csv.writer(subs)
            writer.writerow((email, number))
        # feedback
        return f'{email} subscribed to {number}'

server = xmlrpc.server.SimpleXMLRPCServer(("0.0.0.0", 2412))
server.register_instance(Server())
server.serve_forever()