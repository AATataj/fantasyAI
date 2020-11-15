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
    maxDate = findMaxDate(cursor)
    print(maxDate)
    return

def findMaxDate(cursor):
    query = "select max(date) from boxscores"
    cursor.execute(query)
    return cursor.fetchone()