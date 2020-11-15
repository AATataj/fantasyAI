import time, datetime, json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
from datetime import date
from channels.generic.websocket import WebsocketConsumer
import unidecode
import pdb
from channels.generic.websocket import WebsocketConsumer

def scrape (socket=None):  #def scrape(cnx, socket=None):
    cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba') 
    cursor = cnx.cursor()
    maxDateBox = findMaxDate(cursor)
    today = datetime.date.today()
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    # chrome_opts.add_argument("--headless")
    # driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)
    # get thru accept cookies popup

    linkText = "https://www.nba.com/stats/search/player-game/?SeasonType=Regular%20Season"
    linkText += "&DateFrom="+str(maxDateBox[0].month)+"%2F"+str(maxDateBox[0].day)+"%2F"+str(maxDateBox[0].year)
    linkText += "&DateTo="+str(today.month)+"%2F"+str(today.day)+"%2F"+str(today.year)
    linkText += "&dir=1&sort=GAME_DATE"
    print (linkText)
    driver.get(linkText)
    time.sleep(5)
    cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
    cookies.click()

    clear40Filter = driver.find_element_by_class_name("close")
    clear40Filter.click()
    runIt = driver.find_element_by_class_name("run-it")
    runIt.click()

    time.sleep(10)

    while (1):
        try:
            addRows = driver.find_element_by_class_name("addrows__button")
            addRows.click()
            time.sleep(3)
        except:
            break

    print("we broke out of the loop...yay!")
    time.sleep(10)
    return

def findMaxDate(cursor):
    query = "select max(date) from boxscores"
    cursor.execute(query)
    return cursor.fetchone()