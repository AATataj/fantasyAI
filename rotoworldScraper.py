import time, datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector

import pdb

def updateRoto(cnx):
    #get date of latest entry
    cursor = cnx.cursor()
    query = "select max(date) from rotoworld"
    cursor.execute(query)
    maxDate = cursor.fetchone()
    
    #connect to rotoworld
    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)
    driver.get('https://www.rotoworld.com/basketball/nba/player-news')

    #pull data
    while 1:
        elem = driver.find_elements_by_class_name("player-news-article")
        artcleDate = elem[0].find_element_by_class_name("player-news-article__timestamp").text
        checkDate =  datetime.datetime.strptime(artcleDate[:-3], '%b %d, %Y, %I:%M %p')
        if (checkDate <= maxDate[0]):
            break
        if len(driver.find_elements_by_class_name("player-news-article")) < 10:
            print("loading issue warning")
            time.sleep(10)

        for x in range (len(elem)):
            playerName = elem[x].find_element_by_class_name("player-news-article__profile__name").text
            positionTeam = elem[x].find_element_by_class_name("player-news-article__profile__position").text
            articleTitle = elem[x].find_element_by_class_name("player-news-article__title").text
            try:
                articleSummary = elem[x].find_element_by_class_name("player-news-article__summary").text
            except:
                articleTitle = ""
                continue
            artcleDate = elem[x].find_element_by_class_name("player-news-article__timestamp").text
            checkDate =  datetime.datetime.strptime(artcleDate[:-3], '%b %d, %Y, %I:%M %p')
            
            if (checkDate > maxDate[0]):
                entry = [playerName, positionTeam, articleTitle, articleSummary, checkDate]
                articleTitle = articleTitle.replace('"', "")
                articleTitle = articleTitle.replace("'", "")
                articleSummary = articleSummary.replace('"', "")
                articleSummary = articleSummary.replace("'", "")

                #STR_TO_DATE('{4}', "%Y-%m-%d %H:%i %p"))
                query = """insert into rotoworld (name, posTeam, title, content, date) 
                        values ("{0}", "{1}", "{2}", "{3}", "{4}");
                        """.format(playerName, positionTeam, articleTitle, articleSummary, checkDate.strftime("%Y-%m-%d %H:%M"))
                print (playerName + " : " + positionTeam + "  : " + artcleDate)
                #pdb.set_trace()
                cursor.execute(query)
                cnx.commit()
            
            if (checkDate <= maxDate[0]):
                break
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

        except :
            break
        
    ###
    ### index the new entries here
    ###

    query = """
            update rotoworld
            inner join playerHashes on playerHashes.name = rotoworld.name
            set lower(rotoworld.playerID) = lower(playerHashes.playerID)
            where rotoworld.playerID is null
            """
    cursor.execute(query)
    cnx.commit()

    driver.quit()