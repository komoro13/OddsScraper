import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"
MATCH_DIV_CLASS = "vue-recycle-scroller__item-wrapper"

def download_matches(url, headers):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.maximize_window()
    scroll_y = 0
    while(True):
         scroll_y = driver.execute_script("return window.pageYOffset")
         driver.execute_script("window.scrollBy(0, 1000)")
         sleep(5)
         if (driver.execute_script("return window.pageYOffset") == scroll_y):
              break
    driver.execute_script("window.scrollTo(0, 0)")
    match_divs = driver.find_element(By.CLASS_NAME, MATCH_DIV_CLASS)
    matches_divs_array = match_divs.find_elements(By.XPATH, "*")
    first_element = matches_divs_array[0]
    last_element = matches_divs_array[-1]
    match_str = []
    for match_div in matches_divs_array:
        if match_div.text != "":
            match_str.append(match_div.text)
    return match_str

    
    
    
matches = download_matches(URL, HEADERS)
for match in matches:
      print(match + "\n")