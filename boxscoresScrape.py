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
    #linkText += "&DateFrom="+str(8)+"%2F"+str(11)+"%2F"+str(2020)
    linkText += "&DateTo="+str(today.month)+"%2F"+str(today.day)+"%2F"+str(today.year)
    #linkText += "&DateTo="+str(8)+"%2F"+str(11)+"%2F"+str(2020)
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

    ## variables for progress bar
    updateStartDate = maxDateBox[0]
    updateEndDate = datetime.date.today()
    totalDays = (updateEndDate - updateStartDate).days
    progress = 0
    ## /progress bar vars

    time.sleep(10)

    while (1):
        try:
            addRows = driver.find_element_by_class_name("addrows__button")
            addRows.click()
            time.sleep(3)
        except:
            break
    progress = 10
    print(progress)
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
    for row in range(int(len(tableRows)/2)):
        if row > (len(tableRows)/2):
            break
        if tableRows[row] != tableRows[0]:
            statLine = tableRows[row].find_elements_by_tag_name("td")
            name = statLine[0].text
            nbaID = statLine[0].find_element_by_tag_name('a').get_attribute("href")
            nbaID = re.sub("\D", "", nbaID)
            team = statLine[1].text
            date = statLine[2].text
            date = date[-4:] + '-' + date[:2] + '-' + date[3:5] 
            opponent = statLine[3].text[-3:]
            if statLine[3].text[4]=='@':
                homeAway = '@'
            else:
                homeAway = ""
            result = statLine[4].text
            mins = statLine[5].text
            pts = statLine[6].text
            fgm = statLine[7].text
            fga = statLine[8].text
            if statLine[9].text !='-' :
                fgPer = statLine[9].text
            else :
                fgPer = ''
            threefgm = statLine[10].text
            threefga = statLine[11].text
            if statLine[12].text !='-' :
                threefgPer = statLine[12].text
            else :
                threefgPer = ''
            ftm = statLine[13].text
            fta = statLine[14].text
            if statLine[15].text !='-' :
                ftPer = statLine[15].text
            else :
                ftPer = ''
            orb = statLine[16].text
            drb = statLine[17].text
            trb = statLine[18].text
            ast = statLine[19].text
            stl = statLine[20].text
            blk = statLine[21].text
            tov = statLine[22].text
            pf = statLine[23].text
            plusMinus = statLine[24].text
            twofgm = int(fgm) - int(threefgm)
            twofga = int(fga) - int(threefga)
            if int(twofga) != 0:
                twofgPer = twofgm / twofga
            else : 
                twofgPer = ''
            query = """
                    insert into boxscores 
                    (name, date, team, homeAway, opponent, result, minutes, 
                    fgm, fga, fgPer, 2fgm, 2fga, 2fgPer, 3fgm, 3fga, 3fgPer, ftm, fta, ftPer, 
                    orb, drb, trb, ast, stl, blk, tov, pf, pts, nbaID, plusMinus)
                    values ("{0}","{1}","{2}","{3}","{4}","{5}",{6},{7},{8},{9},{10}
                    {11},{12},{13},{14},{15},{16},{17},{18},{19},{20},{21},
                    {22},{23},{24},{25},{26},{27},{28})    
                    """.format(name, date, team, homeAway, opponent, result, mins,
                        fgm, fga, fgPer, twofgm, twofga, twofgPer, threefgm, threefga, threefgPer,
                        ftm, fta, ftPer, orb, drb, trb, ast, blk, tov, pf, pts, nbaID, plusMinus 
                    )
            if socket != None:
                checkDate = datetime.date(int(date[:4]), int(date[5:7]), int(date[-2:]))
                if progress != 10 + round((100 - (((checkDate - updateStartDate).days)/totalDays) * 100)*0.85, 1):
                    progress = 10 + round((100 - (((checkDate - updateStartDate).days)/totalDays) * 100)*0.85, 1)
                    socket.send(text_data=json.dumps({
                        'progress': progress
                    }))
                    print(progress)
            print(query)
            #cursor.execute(query)
    time.sleep(10)
    progress = 100
    print(progress)
    return

def findMaxDate(cursor):
    query = "select max(date) from boxscores"
    cursor.execute(query)
    return cursor.fetchone()