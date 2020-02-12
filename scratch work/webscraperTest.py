import time, datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import csv


with open('rotoworld.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)
    
    driver.get('https://www.rotoworld.com/basketball/nba/player-news')
    while 1:
        if (len(driver.find_elements_by_class_name("player-news-article__profile__name")) <10 
            or len(driver.find_elements_by_class_name("player-news-article__profile__position")) <10 
            or len(driver.find_elements_by_class_name("player-news-article__title")) <10 
            or len(driver.find_elements_by_class_name("player-news-article__summary")) <10
            or len(driver.find_elements_by_class_name("player-news-article__timestamp")) <10) :
                print("loading issue warning")
                time.sleep(30)
        for x in range (len(driver.find_elements_by_class_name("player-news-article__profile__name"))):
            playerName = driver.find_elements_by_class_name("player-news-article__profile__name")[x].text
            positionTeam = driver.find_elements_by_class_name("player-news-article__profile__position")[x].text
            articleTitle = driver.find_elements_by_class_name("player-news-article__title")[x].text
            articleSummary = driver.find_elements_by_class_name("player-news-article__summary")[x].text
            artcleDate = driver.find_elements_by_class_name("player-news-article__timestamp")[x].text
            print(playerName + " : " + str(x))
            #print (artcleDate[:-3])
            checkDate =  datetime.datetime.strptime(artcleDate[:-3], '%b %d, %Y, %I:%M %p')
            writer.writerow([playerName, positionTeam, articleTitle, articleSummary, artcleDate])
            #if checkDate < datetime.datetime(2019, 4, 5):
                #writer.writerow([playerName, positionTeam, articleTitle, articleSummary, artcleDate])
        try : 
            #nextActive = driver.find_element_by_class_name("next")
            element_present = EC.presence_of_element_located((By.CLASS_NAME, "next"))
            nextActive = WebDriverWait(driver, 30).until(element_present)
            
            nextActive.click()

            element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "player-news-article__profile__name"))
            WebDriverWait(driver, 30).until(element_present)
            element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "player-news-article__profile__position"))
            WebDriverWait(driver, 30).until(element_present)
            element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "player-news-article__title"))
            WebDriverWait(driver, 30).until(element_present)
            element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "player-news-article__summary"))
            WebDriverWait(driver, 30).until(element_present)
            element_present = EC.visibility_of_all_elements_located((By.CLASS_NAME, "player-news-article__timestamp"))
            WebDriverWait(driver, 30).until(element_present)
            
            #time.sleep(2)
        except :
            break
