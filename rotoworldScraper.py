import time, datetime, datetime, json
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from channels.generic.websocket import WebsocketConsumer
import mysql.connector



## I will have to use an intermediary table for updates before committing 
## to the rotoworld live table to save execution time on indexing the players
## against the playerHashes table like I already do for the boxscores.  
## But for now, the rotoworld table is small, and thus not a huge performance hit.
## This is a 'next season' upgrade.  
def updateRoto(cnx, socket=None):
    #get date of latest entry
    
    
    cursor = cnx.cursor()
    query = "select max(date) from rotoworld"
    cursor.execute(query)
    maxDate = cursor.fetchone()

    updateStartDate = maxDate[0]
    updateEndDate = datetime.datetime.today()
    totalDays = (updateEndDate - updateStartDate).days
    progress = 0
    

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
            # remove jr's
            playerName = playerName.replace('JR.', '')
            # remove II and III
            if (playerName != 'JOEL EMBIID'):
                playerName = playerName.replace('II', '')
            playerName = playerName.replace('III', '')
            # remove periods from names
            playerName = playerName.replace('.', '')
            
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

                ## send websocket update
                if socket != None:
                    if progress != round(100 - (((checkDate - updateStartDate).days)/totalDays) * 100, 1):
                        progress = round(100 - (((checkDate - updateStartDate).days)/totalDays) * 100, 1)
                        socket.send(text_data=json.dumps({
                            'progress': progress
                        }))
                ## /update
    

                #STR_TO_DATE('{4}', "%Y-%m-%d %H:%i %p"))
                query = """insert into rotoworld (name, posTeam, title, content, date) 
                        values ("{0}", "{1}", "{2}", "{3}", "{4}");
                        """.format(playerName, positionTeam, articleTitle, articleSummary, checkDate.strftime("%Y-%m-%d %H:%M"))
                print (playerName + " : " + positionTeam + "  : " + artcleDate)
                
                #########
                # uncomment these
                #########
                #cursor.execute(query)
                #cnx.commit()
            
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

            ## note the below query will not suit our purposes when :
            ## 2 or more players have the same name and are playing in the same season
            ## in that case, it'll match to the younger player and ignore the older one
            ## this case has come up 3x seperate times in previous years, but currently isn't 
            ## an issue.  A strategy for dealing with this, would be to update our playerHashes 
            ## table with the player's current team, and match with that data like we do 
            ## birthdays in the boxscores, but particular attention must be paid to 
            ## rotoworld articles that indicate player trades, as that team may change on the 
            ## article which announces the trade

    query = """
            update rotoworld
            inner join 
                (select name, dob, playerID
                from playerHashes
                    inner join  
                        (select name as named, max(dob) as Dateob, count(name) 
                        from playerHashes 
                        group by name 
                        having max(dob)) 
                        as list 
                    on list.named = playerHashes.name and list.Dateob = playerHashes.dob) as joined
            on joined.name = rotoworld.name
            set rotoworld.playerID = joined.playerID
            where rotoworld.playerID is null
            """
            

    ###########cursor.execute(query)
    ###########cnx.commit()

    # we need manual fixes for luka doncic, juancho hernangomez, taurean prince and jj redick cuz 
    # the names don't match boxscores data and it's never easy...
    # indivdual cases can be removed once the player is out of the league.  
    # I'm looking at you, JJ....stupid dukkies, who drafts them anyway?
    query = """
            update rotoworld
            set playerID = 1919
            where name = 'LUKA DONCIC'
            """
    cursor.execute(query)
    cnx.commit()

    query = """
            update rotoworld
            set playerID = 1622
            where name = 'JUANCHO HERNANGOMEZ'
            """
    cursor.execute(query)
    cnx.commit()

    query = """
            update rotoworld
            set playerID = 1234
            where name = 'JJ REDICK'
            """
    cursor.execute(query)
    cnx.commit()

    query = """
            update rotoworld
            set playerID = 2815
            where name = 'TAUREAN PRINCE'
            """
    cursor.execute(query)
    cnx.commit()


    driver.quit()