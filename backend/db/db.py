import sqlite3, os

database = os.path.join(os.path.dirname(__file__), './../data/subscriptions.db')
conn = sqlite3.connect(database)
cur = conn.cursor()

def changes_made():
    cur.execute('SELECT changes()')
    return bool(cur.fetchone()[0])
