import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import random

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"
MATCH_DIV_CLASS = "vue-recycle-scroller__item-wrapper"
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
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.maximize_window()
    scroll_y = 0
    matches_divs_array = []
    x = 0
    match_str_array = []
    while(True):
         scroll_y = driver.execute_script("return window.pageYOffset")
         scroll = random.randint(200, 300 )
         driver.execute_script("window.scrollBy(0, "+ str(scroll) + ")")
         if (driver.execute_script("return window.pageYOffset") == scroll_y):
              break
         try:
            match_divs = driver.find_element(By.CLASS_NAME, MATCH_DIV_CLASS)
         except:
            break
         print("------------------" + str(x) + "-------------------")
         if (match_divs.text == ""):
              break
         matches_divs_array = matches_divs_array + match_divs.find_elements(By.XPATH, "*")
         for matches_div in matches_divs_array:
             if matches_div.text == "":
                 matches_divs_array.remove(matches_div)
         for match_div in matches_divs_array:
              match_str_array.append(match_div.text)
         x = x + 1   
    match_str_array = list(filter(None, match_str_array))
    found_one = False
    for match_str in match_str_array:
         print(len(match_str.split("\n")))
         if len(match_str.split("\n")) < 5:
             print("deleting: " + match_str.replace("\n", " "))
             match_str_array.remove(match_str)
             continue
         for match_st in match_str_array:
               print ("----------------------------------\n" + match_st.replace("\n", " ") + "\n?=\n" + match_str.replace("\n", " ") + "\n--------------------------------" )
               if match_str == match_st:
                    print(found_one)
                    if found_one == True:
                        print("removing: " + match_st)
                        match_str_array.remove(match_st)
                        continue
                    found_one = True
         found_one = False 
    for match_s in match_str_array:
         print("match_str: " + str(match_str_array.index(match_s)) + " " + match_s.replace("\n", " "))
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
     match = Match_DAT(match_data[0], match_data[2] + "-" + match_data[3], over, under)
     return match

def sendMessage(match_str):
     print(requests.get(TELEGRAM_URL + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + match_str).json())

matches = []

while(True):
     matches_str = download_matches(URL, HEADERS)
     print(matches_str)
     for match_str in matches_str:
          match_s = addMatchToMathes(match_str)
          for match in matches:
               if match_s.match_name == match.match_name:
                    if match.getMatchMessagge != "":
                      sendMessage(match.getMatchMessage())
                      matches.remove(match)
                    elif WRITE_TIME - 10 < match.getTimeDifference < WRITE_TIME:
                         matches.append(match_s)