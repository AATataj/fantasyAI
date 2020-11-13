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
import re
import pdb

cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

driver = webdriver.Chrome('/usr/bin/chromedriver')
chrome_opts = Options()
#chrome_opts.add_argument("--headless")
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)

driver.get("https://www.nba.com/players")
time.sleep(5)
cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
cookies.click()

historic = driver.find_element_by_class_name("Toggle_slider__hCMQQ")
historic.click()
time.sleep(2)

## hit the next button : 
#nextButton = driver.find_elements_by_class_name("Pagination_button__1MPZe")
#print(nextButton[0].is_enabled())
#nextButton[1].click()

## pull data per row :
playerTable = driver.find_element_by_class_name("PlayerList_playerTable__3SEob")
tableRows = driver.find_elements_by_tag_name("tr")
print(len(tableRows))
while (1):
    tableRows = driver.find_elements_by_tag_name("tr")
    for row in tableRows :
        if row != tableRows[0]:
            name = row.find_elements_by_tag_name('td')[0].find_elements_by_tag_name('p')[0].text
            name = name + " " + row.find_elements_by_tag_name('td')[0].find_elements_by_tag_name('p')[1].text
            nbaID = row.find_elements_by_tag_name('td')[0].find_element_by_tag_name('a').get_attribute("href")
            nbaID = re.sub("\D", "", nbaID)
            college = row.find_elements_by_tag_name('td')[6].text
            print(name + " " + college + " " + nbaID) 
            query = """
                    insert into nbaHashes (name, college, nbaID) values ("{0}", "{1}", {2});
                    """.format(name, college, nbaID)
            cursor.execute(query)
    nextButton = driver.find_elements_by_class_name("Pagination_button__1MPZe")
    if nextButton[1].is_enabled():
        time.sleep(4)
        nextButton[1].click()
    else:
        break

cnx.commit()
driver.quit()