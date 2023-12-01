from bs4 import BeautifulSoup
import requests

def scrape(number: int):
    return False

page = 'http://www.lions-club-pulheim.de/adventskalender_gewinne.php'
r = requests.get(page)
soup = BeautifulSoup(r.text, 'html.parser')
table = soup.find('table', class_ = 'adventtable')
rows = table.find_all('tr')

columns = []
for row in rows:
    for col in row.find_all('th'):
        columns.append(col.text)
        
wins = []
for row in rows:
    data = {}
    for col, val in zip(columns, row.find_all('td')):
        data[col] = val.text
    wins.append(data)

for win in wins:
    for key, value in win.items():
        print(key, ':', value)