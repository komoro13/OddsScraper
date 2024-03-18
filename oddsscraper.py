import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"
MATCH_DIV_CLASS = "vue-recycle-scroller__item-wrapper"
TOKEN = "6589363155:AAHegC4NDTAChKUQLMtXpsNKl8zGeIaGgs0"
TELEGRAM_URL = "https://api.telegram.org/bot" 
CHAT_ID = "-1001751992895"
TIME_FORMAT = "%H:%M"


class Match_DAT:
     match_name  = ""
     match_time = ""
     match_over = ""
     match_under = ""
     THRESHOLD = 20
     MINUTES_SAVE = 120
     MINUTES_CHECK = 10
     def __init__(self, name, time, over, under):
          self.match_name = name
          self.match_time = time
          self.match_over = over
          self.match_under = under
     def printMatchString(self):
          print (self.match_name + " Time: " + self.match_time + " Over: " + self.over + " Under: " + self.under)
     def getTimeDifference(self):
          d1 = datetime.strptime(self.match_time, TIME_FORMAT)
          d2 = datetime.now().time
          return (d1-d2).seconds/60
     
     def checkOver(self, over_n):
          percentage = (100*(self.over-over_n))/self.checkOver
          if (percentage > self.THRESHOLD):
               return percentage
          else:
               return -1
     
        
def download_matches(url, headers):
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.maximize_window()
    scroll_y = 0
    matches_divs_array = []
    x = 0
    while(True):
         scroll_y = driver.execute_script("return window.pageYOffset")
         driver.execute_script("window.scrollBy(0, 200)")
         sleep(5)
         try:
            match_divs = driver.find_element(By.CLASS_NAME, MATCH_DIV_CLASS)
         except:
            break
         print("------------------" + str(x) + "-------------------")
         matches_divs_array = matches_divs_array + match_divs.find_elements(By.XPATH, "*")
         for matches_div in matches_divs_array:
             if matches_div.text == "":
                 matches_divs_array.remove(matches_div)
         x = x + 1
         print(len(matches_divs_array))    
         if (driver.execute_script("return window.pageYOffset") == scroll_y):
              break
    match_str_array = []
    for match_div in matches_divs_array:
                match_str_array.append(match_div.text)
    print(matches_divs_array.text)
    found_one = False
    for match_str in match_str_array:
        for match_st in match_str_array:
             if match_str == match_st:
                 if found_one == True:
                      match_str_array.remove(match_st)
                 else:
                      found_one == False
        found_one = False
    return match_str_array

def addMatchToMathes(match_str):
     match_data = match_str.split("\n")
     over = ""
     under = ""
     for attr in match_data:
          if attr.split(" ")[0] == "O":
               over = match_data[match_data.index(attr) + 1]
          if attr.split(" ")[0] == "U":
               under = match_data[match_data.index(attr) + 1]
     match = Match_DAT(match_data[0], match_data[2] + "-" + [match_data[3]], over, under)
     return match
def sendMessage(match_str):
     print(requests.get(TELEGRAM_URL + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + match_str).json())

matches_str = download_matches(URL, HEADERS)
matches = []
for match_str in matches_str:
     match_s = addMatchToMathes(match_str)
     sendMessage(match_s.match_name)
               