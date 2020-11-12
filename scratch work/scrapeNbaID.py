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

# cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
# cursor = cnx.cursor()

driver = webdriver.Chrome('/usr/bin/chromedriver')
chrome_opts = Options()
#chrome_opts.add_argument("--headless")
driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)

driver.get("https://www.nba.com/players")
time.sleep(5)
cookies = driver.find_element_by_id("onetrust-accept-btn-handler")
cookies.click()

historic = driver.find_element_by_name("showHistoric")
historic.click()

#<button id="onetrust-accept-btn-handler" tabindex="0">I Accept</button>