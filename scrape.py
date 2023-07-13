import requests
from bs4 import BeautifulSoup

r = requests.get("https://timesofindia.indiatimes.com/briefs")
soup = BeautifulSoup(r.content, 'html.parser')

headings = soup.find_all('h2')

headings = headings[0:-13]

for h in headings:
    print(h.get_text())