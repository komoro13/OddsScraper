import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"

def download_matches(url, headers):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.maximize_window()
    
matches = download_matches(URL, HEADERS)
for match in matches:
      print(match + "\n")