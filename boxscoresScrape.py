import time, datetime, json, re
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
    
    tableRows= driver.find_elements_by_tag_name("tr")

    """
   NOTE : NBA.COM doesn't label the <td> elements in it's stats tables.
          In case they do something dum like changing the order/content 
          of those tables, this is the current map between indices -> categories  
        0: player name  6: pts  12: 3%  18: trb 24: +/- 
        1: team         7: fgm  13: ftm 19: ast
        2: date         8: fga  14: fta 20: stl
        3: opp          9: fg%  15: ft% 21: blk
        4: w/l          10:3pm  16: orb 22: tov
        5: mins         11:3pa  17: drb 23: pf
    """
    for row in tableRows:
        if row != tableRows[0]:
            statLine = row.find_elements_by_tag_name("td")
            name = statLine[0].text
            nbaID = statLine[0].find_element_by_tag_name('a').get_attribute("href")
            nbaID = re.sub("\D", "", nbaID)
            team = statLine[1].text
            print (name + "," + str(nbaID) +"," + team)
    time.sleep(10)
    return

def findMaxDate(cursor):
    query = "select max(date) from boxscores"
    cursor.execute(query)
    return cursor.fetchone()