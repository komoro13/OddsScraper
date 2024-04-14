import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import random
import time
import os
import undetected_chromedriver
import pandas

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
URL = "https://en.stoiximan.gr/sport/soccer/next-3-hours/"
MATCH_DIV_CLASS = "vue-recycle-scroller__item-wrapper"
COOKIES_ACCEPT_BTN = "onetrust-accept-btn-handler"

TOKEN = ""
TELEGRAM_URL = "https://api.telegram.org/bot" 
CHAT_ID = ""

FILENAME = ""

TIME_FORMAT = "%H:%M"
WRITE_TIME = 120

class Match_DAT:
     match_name  = ""
     match_time = ""
     match_over = ""
     match_under = ""
     match_x = ""
     match_1 = ""
     match_2 = ""
     match_over_goals = ""
     match_under_goals = ""
     #excel_data = []
     THRESHOLD = 10
     def __init__(self, name, time, over, under, x, assos, diplo, over_goals, under_goals):
          self.match_name = name
          self.match_time = time
          self.match_over = over
          self.match_under = under
          self.match_x = x
          self.match_1 = assos
          self.match_2 = diplo
     def printMatchString(self):
          print (self.match_name + " Time: " + self.match_time + " Over: " + self.over + " Under: " + self.under)
     def getTimeDifference(self):
          d1 = datetime.strptime(self.match_time, TIME_FORMAT)
          d2 = datetime.strptime(time.strftime(TIME_FORMAT, time.localtime()), TIME_FORMAT)
          return (d1-d2).total_seconds()/60
     
     def checkOver(self, over_n):
          if self.match_over == "" or over_n == "":
               return -1  
          percentage = round(100*((float(over_n)) - float(self.match_over))/float(self.match_over), 2)
          if (abs(percentage) > self.THRESHOLD):
               return str(percentage)
          else:
               return -1
          
     def checkUnder(self, under_n):
          if self.match_under == "" or under_n == "":
               return -1
          percentage = round(100*((float(under_n) - float(self.match_under) ))/float(self.match_under), 2)
          if (abs(percentage) > self.THRESHOLD):
               return str(percentage)
          else: 
               return -1
          
     def checkX(self, x_n):
          if self.match_x == "" or not x_n == "":
               return -1
          percentage = round(100*((float(x_n) - float(self.match_x) ))/float(self.match_x), 2)
          if (abs(percentage) > self.THRESHOLD):
               return str(percentage)
          else: 
               return -1
          
     def check1(self, assos_n):
          if self.match_1 == "" or assos_n == "":
               return -1
          percentage = round(100*((float(assos_n) - float(self.match_1) ))/float(self.match_1), 2)
          if (abs(percentage) > self.THRESHOLD):
               return str(percentage)
          else: 
               return -1
          
     def check2(self, diplo_n):
          if self.match_2 == "" or not diplo_n == "":
               return -1
          percentage = round(100*((float(diplo_n) - float(self.match_2) ))/float(self.match_2), 2)
          if (abs(percentage) > self.THRESHOLD):
               return str(percentage)
          else: 
               return -1
          
     def checkOverGoals(self, over_goals_n):
          if self.match_over_goals == "" or over_goals_n == "":
               return False
          if self.match_over_goals != over_goals_n:
               return True
          return False
          
     def checkUnderGoals(self, under_goals_n):
          if self.match_over_goals == "" or under_goals_n == "":
               return False
          if self.match_under_goals != under_goals_n:
               return True
          return False
          
     def getMatchMessage(self, over, under, x, assos, diplo, over_goals, under_goals):
          c_over = float(self.checkOver(over))
          c_under = float(self.checkUnder(under))
          
          c_x = float(self.checkX(x))
          c_1 = float(self.check1(assos))
          c_2 = float(self.check2(diplo))
          
          c_over_goals = self.checkOverGoals(over_goals)
          c_under_goals = self.checkUnderGoals(under_goals)

          if c_over == -1 and c_under == -1 and c_x == -1 and c_1 == -1 and c_2 == -1 and not c_over_goals and not c_under_goals:
               return ""
          
          match_message = "Match " + self.match_name + " has\n "

          if (c_over_goals == True):
               match_message += "a change in over as previous over was over " + self.match_over_goals + "and now it is over " + over_goals 
          if (c_under_goals == True ):
               match_message += " and a change in under as previous under was under " + self.match_under_goals + "and now it is under " + under_goals
          
          if c_over != -1 and  not c_over_goals:
               match_message += str(c_over) + " % "
               if c_over > 0:
                    match_message += " Rise in Over " + self.match_over_goals + " \n"
                    try:
                         self.excel_data.append({"sheet":"Rise in Over"})
                    except Exception as e:
                         sendMessage(str(e))
               else:
                    match_message += " Drop in Over" + self.match_over_goals + " \n"
               match_message += " \n Previous Over: " + self.match_over + " Current over: " + over + "\n"

          if c_under != -1 and not c_under_goals:
               match_message +=  str(c_under) + " % "
               if c_under > 0:
                    match_message += " Rise in Under " + self.match_under_goals +" \n "
               else:
                    match_message += " Drop in Under " + self.match_under_goals + " \n"
               match_message += " \n Previous Under: " + self.match_under + " Current under: " + under + "\n"
               

          if c_x != -1:
               match_message += str(c_x) + " % "
               if c_x > 0:
                    match_message += " Rise in x\n"
               else:
                    match_message += " Drop in x\n"
               match_message += " \n Previous X: " + self.match_x + " Current X: " + over + "\n"
          if c_1 != -1:
               match_message += str(c_1) + " % "
               if c_1 > 0:
                    match_message += " Rise in 1\n"
               else:
                    match_message += " Drop in 1\n"
               match_message += " \n Previous 1: " + self.match_1 + " Current 1: " + assos + "\n"

          if c_2 != -1:
               match_message += str(c_2) + " % "
               if c_2 > 0:
                    match_message += " Rise in 2\n"
               else:
                    match_message += " Drop in 2\n" 
               match_message += " \n Previous 2: " + self.match_2 + " Current 2: " + diplo + "\n"
          
          match_message += ", so it worths suggesting it."
          
          return match_message
     

def get_creds(filename):
     file = open(filename, 'r')
     Lines = file.readlines()
     chat_id = Lines[0]
     token = Lines[1]
     filename = Lines[2]
     creds = {"chat_id":chat_id, "token":token, "filename":filename}
     return creds

def download_matches(url, headers):
    
     try:
          driver = undetected_chromedriver.Chrome() #init driver
          driver.get(URL) #get request to webpage
          driver.maximize_window() #maximize window so the height of each div is fixed

          scroll_y = 0 #Height of the page
          matches_divs_array = [] #WebElements array of matches divs
          x = 0
          match_str_array = [] #Str array of matches divs text

          while(True):          
                         scroll_y = driver.execute_script("return window.pageYOffset") #getting the height of the page
                         driver.execute_script("window.scrollBy(0, 300)") #scrolling by 300 px so it does load all the mactches of each scroll
                         if (driver.execute_script("return window.pageYOffset") == scroll_y): #if current position is equal to page bottom exit loop
                              break
                         try:
                              match_divs = driver.find_element(By.CLASS_NAME, MATCH_DIV_CLASS) #find the div that has the matches, if cannot find exit loop
                         except:
                              break
                         if (match_divs.text == ""): #if text of matches div is empty exit loop
                              break
                         matches_divs_array = matches_divs_array + match_divs.find_elements(By.XPATH, "*") #get an array of divs from the main div 
                         
                         for match_div in matches_divs_array: #convert the WebElement array to an Str array
                              match_str_array.append(match_div.text)
                         
                         matches_divs_array = [] #empty the WebElement array
                         x = x + 1

          driver.close() #since finished loading close the driver

          match_str_array = list(filter(None, match_str_array)) #filter matches and remove empty strings
                         

          #This loop removes matches loaded more than once

          found_one = False #Found first occurence of a match in the array

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
     
     except:
          try:
               driver.close()
          except:
               return ""
          return ""
                    

def addMatchToMatches(match_str):
     match_data = match_str.split("\n")
     over = ""
     under = ""
     x = ""
     assos = ""
     diplo = ""
     over_goals = ""
     under_goals = ""
     try:
          datetime.strptime(match_data[1], TIME_FORMAT)
     except:
          return ""
     try:     
          if  "." in match_data[4]:
               assos = match_data[4]
               x = match_data[5]
               diplo = match_data[6]
     except :
          x = ""
          assos = ""
          diplo = ""

     try:
          for attr in match_data:
               if attr.split(" ")[0] == "O":
                    over = match_data[match_data.index(attr) + 1]
                    over_goals = attr.split(" ")[1]
                    if over_goals == "":
                         exit(-1)
               if attr.split(" ")[0] == "U":
                    under = match_data[match_data.index(attr) + 1]
                    under_goals = attr.split(" ")[1]
               match = Match_DAT(match_data[2] + "-" + match_data[3],match_data[1], over, under,x, assos, diplo, over_goals, under_goals)
     except:
          over = ""
          under = ""
          over_goals = ""
          under_goals = ""
     
     return match

def sendMessage(match_str):
     print(requests.get(TELEGRAM_URL + TOKEN + "/sendMessage?chat_id=" + CHAT_ID + "&text=" + match_str).json())

def appendMatchToExcel(match_dict):
     filename = FILENAME
     sheet = match_dict["sheet"]
     data = match_dict["data"]


def addMatchesToList():
     while(len(matches) == 0):
          for match_str in download_matches(URL, HEADERS):
               if len(match_str.split("\n")) > 5 and "/" in match_str and ":" in match_str:
                    match = addMatchToMatches(match_str)
                    if match == "":
                         continue
                    if WRITE_TIME - 20 < match.getTimeDifference() < WRITE_TIME + 20:
                         matches.append(match)
     return

def displayData():
     os.system("cls")
     print("Current data")
     print("Matches loaded: " + str(len(matches)))
     print("Downloads: " + str(downloads))
     print("Matches: ")
  
creds = get_creds("creds.txt")

CHAT_ID = creds["chat_id"]
TOKEN = creds["token"]
FILENAME = creds["filename"]

matches = []
downloads = 0

print("Wait till a match is added")
     
found = False

while(True):
     if len(matches) == 0:
          addMatchesToList()
     matches_str = download_matches(URL, HEADERS)
     downloads = downloads + 1

     for match_str in matches_str:
          found = False
          if len(match_str.split("\n")) > 5 and "/" in match_str and ":" in match_str:
               match_s = addMatchToMatches(match_str)
          if match_s == "":
               continue
          for match in matches:
               if match.getTimeDifference() < 0:
                    matches.remove(match)
               if match_s.match_name == match.match_name:
                     found = True
                     match_message = match.getMatchMessage(match_s.match_over, match_s.match_under, match_s.match_x, match_s.match_1, match_s.match_2, match_s.match_over_goals, match_s.match_under_goals)
                     if match_message != "":
                         sendMessage(match_message)
                         matches.remove(match)
          if found == False and WRITE_TIME - 20 < match.getTimeDifference() < WRITE_TIME + 20:
                         matches.append(match_s)
     displayData()     