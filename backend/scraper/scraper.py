from bs4 import BeautifulSoup
import requests, datetime

class Scraper():
    
    url = 'http://www.lions-club-pulheim.de/adventskalender_gewinne.php'
    
    def __init__(self):
        # get HTML
        page = requests.get(self.url)

        # parse
        soup = BeautifulSoup(page.text, 'html.parser')
        table = soup.find('table', class_ = 'adventtable')
        rows = table.find_all('tr')

        # headers
        columns = []
        for row in rows:
            for col in row.find_all('th'):
                columns.append(col.text)
        
        # wins
        self.wins = []
        for row in rows:
            data = {}
            for col, val in zip(columns, row.find_all('td')):
                data[col] = val.text
            self.wins.append(data)

    def result(self, number: int):
        # determine if won
        for win in self.wins:
            if win and int(win['Tag']) == datetime.datetime.today().day and int(win['Nummer']) == number:
                # yes
                return f"'{win['Preis']}' gesponsert von '{win['Sponsor']}'"
        # no
        return False