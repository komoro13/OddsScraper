import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import random
from humancursor import WebCursor

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"
MATCH_DIV_CLASS = "vue-recycle-scroller__item-wrapper"
COOKIES_ACCEPT_BTN = "onetrust-accept-btn-handler"
TOKEN = "6589363155:AAHegC4NDTAChKUQLMtXpsNKl8zGeIaGgs0"
TELEGRAM_URL = "https://api.telegram.org/bot" 
CHAT_ID = "-1001751992895"
TIME_FORMAT = "%H:%M"
WRITE_TIME = 120

class Match_DAT:
     match_name  = ""
     match_time = ""
     match_over = ""
     match_under = ""
     THRESHOLD = 10
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
          percentage = (100*(self.over-over_n))/self.over
          if (percentage > self.THRESHOLD):
               return percentage
          else:
               return -1
     def checkUnder(self, under_n):
          percentage = (100*(self.under-under_n))/self.match_under
          if (percentage > self.THRESHOLD):
               return percentage
          else: 
               return -1

     def getMatchMessage(self, over, under):
          c_over = self.checkOver(over)
          c_under = self.checkUnder(under)
          time_ok = self.getTimeDifference() < 5
          if c_over == -1 and c_under == -1 and not time_ok:
               return ""
          match_message = "Match " + self.match_name + "has " 
          if c_over != -1:
               match_message += c_over + "%"
               if self.checkOver > 0:
                    match_message += " Rise in Over"
               else:
                    match_message += " Drop in Over"
          if c_under != -1:
               match_message += " and " + self.checkOver + "%"
               if c_under > 0:
                    match_message += "Rise in Under"
               else:
                    match_message += "Drop in Under"
          match_message = ", so it worths suggesting it."
def download_matches(url, headers):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomatationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(options=options)

    driver.execute_script("Object.defineProperty(navigator, 'webdriver',{get: () => undefined})")
    
    driver.get(URL)
    driver.maximize_window()
    driver.implicitly_wait(1)

    cookies_btn = driver.find_element(By.ID, COOKIES_ACCEPT_BTN)
    cr = WebCursor(driver)
    cr.move_to(cookies_btn)
    cr.click_on(cookies_btn)
    
    scroll_y = 0
    scroll_pos = 0
    matches_divs_array = []
    x = 0
    match_str_array = []
    while(True):
          try:
               scroll_y = driver.execute_script("return window.pageYOffset")
               scroll = random.randint(200, 300 )
               scroll_pos = scroll_pos + scroll
               driver.execute_script("window.scrollTo(0, "+ str(scroll_pos) + ")")
               if (driver.execute_script("return window.pageYOffset") == scroll_y):
                    break
               try:
                   match_divs = driver.find_element(By.CLASS_NAME, MATCH_DIV_CLASS)
               except:
                    break
               if (match_divs.text == ""):
                    break
               matches_divs_array = matches_divs_array + match_divs.find_elements(By.XPATH, "*")
               for match_div in matches_divs_array:
                    match_str_array.append(match_div.text)
               x = x + 1
          except:
               scroll_pos = scroll_pos - scroll
               continue
                   
    match_str_array = list(filter(None, match_str_array))
    found_one = False
    for iter in range(0, len(match_str_array) - 1):
         if iter == len(match_str_array):
              break
         for itr in range(0, len(match_str_array) - 1):
               if itr >= len(match_str_array) or iter >= len(match_str_array):
                    break
               if match_str_array[iter] == match_str_array[itr]:
                    if found_one == True:
                        match_str_array.remove(match_str_array[itr])
                        continue
                    found_one = True
         found_one = False 
    return match_str_array

def addMatchToMatches(match_str):
     match_data = match_str.split("\n")
     over = ""
     under = ""
     for attr in match_data:
          if attr.split(" ")[0] == "O":
               over = match_data[match_data.index(attr) + 1]
          if attr.split(" ")[0] == "U":
               under = match_data[match_data.index(attr) + 1]
          match = Match_DAT(match_data[2] + "-" + match_data[3],match_data[0], over, under)
     return match

def sendMessage(match_str):
     print(requests.get(TELEGRAM_URL + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + match_str).json())

matches = []
while(len(matches) == 0):
     for match_str in download_matches(URL, HEADERS):
          if len(match_str.split("\n")) > 5:
               match = addMatchToMatches(match_str)
          if WRITE_TIME - 10 < match.getTimeDifference() < WRITE_TIME + 10:
               matches.append(match)
while(True):
     matches_str = download_matches(URL, HEADERS)
     for match_str in matches_str:
          if len(match_str.split("\n")) > 5:
               match_s = addMatchToMatches(match_str)
          for match in matches:
               if match.getTimeDifference() < 0:
                    matches.remove(match)
               if match_s.match_name == match.match_name:
                     if match.getMatchMessage() != "":
                         sendMessage(match.getMatchMessage())
                         matches.remove(match)
                     elif WRITE_TIME - 10 < match.getTimeDifference < WRITE_TIME + 10:
                         matches.append(match_s)