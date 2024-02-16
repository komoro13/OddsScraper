import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"


#page = requests.get(URL, headers=HEADERS)
#soup = BeautifulSoup(page.text, 'html.parser')
#print(soup)
#print(page.text)

def download_matches(url, headers):
    page = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(page.text, 'html.parser')
    print(soup)



download_matches(URL, HEADERS)