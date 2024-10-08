# scraper.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, 'html.parser')

        contests = []
        for contest in soup.find_all('div', class_='contest-item'):
            title = contest.find('h2').text
            link = contest.find('a')['href']
            deadline = contest.find('span', class_='deadline').text
            contests.append({'title': title, 'link': link, 'deadline': deadline})
        
        return contests

    def clean_data(self, contests):
        df = pd.DataFrame(contests)

        # Clean and convert deadline format
        df['deadline'] = pd.to_datetime(df['deadline'], errors='coerce')

        # Filter contests based on specific keywords (macro/nature photography)
        df = df[df['title'].str.contains('macro|nature', flags=pd.Series(re.I), regex=True)]

        return df
