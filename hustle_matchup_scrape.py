import time, datetime, json, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait, Select
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
    # set up cnx details
    cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba') 
    cursor = cnx.cursor()

    # get the dappropriate link dates
    #maxDateHustle = findMaxDate(cursor)
    ##
    maxDateHustle = []
    maxDateHustle.append(datetime.date(2018, 2, 20))
    ##

    #today = datetime.date.today()
    ##
    today = datetime.date(2018, 3, 5) 
    ##

    # set up the chromedriver
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    # compile the link
    "https://www.nba.com/stats/search/team-game/?SeasonType=Regular%20Season&DateFrom=03%2F03%2F1997&DateTo=03%2F03%2F1997&sort=GAME_DATE&dir=1"
    linkText = "https://www.nba.com/stats/search/team-game/?SeasonType=Regular%20Season"
    linkText += "&DateFrom="+str(maxDateHustle[0].month)+"%2F"+str(maxDateHustle[0].day)+"%2F"+str(maxDateHustle[0].year)
    linkText += "&DateTo="+str(today.month)+"%2F"+str(today.day)+"%2F"+str(today.year)
    linkText += "&dir=1&sort=GAME_DATE"

    print(linkText)
    driver.get(linkText)
    time.sleep(5)
    # accept cookies, clear filters, run search
    cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
    cookies.click()
    clear130Filter = driver.find_element_by_class_name("close")
    clear130Filter.click()
    runIt = driver.find_element_by_class_name("run-it")
    runIt.click()
    
    # get all results to appear on screen
    time.sleep(10)
    while (1):
        try:
            addRows = driver.find_element_by_class_name("addrows__button")
            addRows.click()
            time.sleep(3)
        except:
            break
    # get the gameID and date for each entry
    tableRows= driver.find_elements_by_tag_name("tr")
    games = []
    for row in range(int(len(tableRows)/2)):
        if tableRows[row] != tableRows[0]:
            if '@' in tableRows[row].find_elements_by_tag_name('td')[2].text:
                games.append((tableRows[row].find_elements_by_tag_name('td')[2].text, 
                tableRows[row].find_elements_by_tag_name('td')[1].text,
                tableRows[row].find_elements_by_tag_name('td')[2].find_element_by_tag_name('a').get_attribute("href")))


    for game in games:
        driver.get(str(game[2]))
        getHustle(driver, cnx, cursor, game[1], socket)

    driver.quit()
    return

def getHustle (driver, cnx, cursor, date, socket=None):
    select = Select(driver.find_element_by_name('splits'))
    print(date)
    for option in select.options:
        if 'Hustle' == option.text:
            select.select_by_value('hustle')
            tableRows = driver.find_elements_by_tag_name('tr')
            for row in range(int(len(tableRows)/2)):
                if tableRows[row] != tableRows[0]:
                    print(tableRows[row].text)
    ## error here, stale element... ?
    pdb.set_trace()

    # tableRows = driver.find_elements_by_tag_name('tr')
    # for row in range(int(len(tableRows)/2)):
    #     print(tableRows[row].text)
    
    return


def findMaxDate(cursor):
    query = "select max(date) from hustle"
    cursor.execute(query)
    return cursor.fetchone()