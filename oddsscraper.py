import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"

def download_matches(url, headers):
    driver = webdriver.Chrome()
    driver.get(URL)
    matches_div = driver.find_elements(By.CLASS_NAME, "vue-recycle-scroller__item-wrapper")
    matches_str = []
    for match_div in matches_div:
           matches_str.append(match_div.text)
    driver.close()
    return matches_str
    

matches = download_matches(URL, HEADERS)
print(matches)
