# google_scraper.py
import requests
from bs4 import BeautifulSoup
import re

class GoogleScraper:
    def __init__(self):
        self.google_search_url = "https://www.google.com/search?q={query}&num={num_results}"

    def search(self, query, num_results=10):
        search_url = self.google_search_url.format(query=query.replace(' ', '+'), num_results=num_results)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(search_url, headers=headers)
        if response.status_code == 200:
            return self.parse_results(response.content)
        else:
            return []

    def parse_results(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                # Google result links may contain junk URLs, filter them
                if re.search(r'^https?://', link):
                    results.append(link)
        return results
