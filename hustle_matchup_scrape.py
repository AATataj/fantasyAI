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
        # getHustle(driver, cnx, cursor, game[1], socket)
        getMatchups(driver, cnx, cursor, game[1], socket)
        pdb.set_trace()
    driver.quit()
    return

def getHustle (driver, cnx, cursor, date, socket=None):
    select = Select(driver.find_element_by_name('splits'))
    formattedDate = datetime.date(int(date[:4]), int(date[5:7]), int(date[-2:]))
    for option in select.options:
        if 'Hustle' == option.text:
            select.select_by_value('hustle')
            tables = driver.find_elements_by_tag_name('tbody')
            for table in tables:
                tableRows = table.find_elements_by_tag_name('tr')
                for row in range(len(tableRows)):
                    player = tableRows[row].find_elements_by_tag('td')[0].text
                    nbaID = tableRows[row].find_elements_by_tag('td')[0].find_elements_by_tag('a').get_attribute('href')
                    mins = tableRows[row].find_elements_by_tag('td')[1].text
                    screen_ast = tableRows[row].find_elements_by_tag('td')[2].text
                    screen_ast_pts = tableRows[row].find_elements_by_tag('td')[3].text
                    deflections = tableRows[row].find_elements_by_tag('td')[4].text
                    off_loose_balls = tableRows[row].find_elements_by_tag('td')[5].text
                    def_loose_balls = tableRows[row].find_elements_by_tag('td')[6].text
                    loose_balls = tableRows[row].find_elements_by_tag('td')[7].text
                    charges_drawn = tableRows[row].find_elements_by_tag('td')[8].text
                    two_contests = tableRows[row].find_elements_by_tag('td')[9].text
                    three_contests = tableRows[row].find_elements_by_tag('td')[10].text
                    shot_contests = tableRows[row].find_elements_by_tag('td')[11].text
                    off_boxouts = tableRows[row].find_elements_by_tag('td')[12].text
                    def_boxouts = tableRows[row].find_elements_by_tag('td')[13].text
                    boxouts = tableRows[row].find_elements_by_tag('td')[14].text
                    query = """
                            insert into hustle
                            (nbaID, name, date, mins, screen_ast, screen_ast_pts, deflections,
                            off_loose_balls, def_loose_balls, loose_balls, charges_drawn, 
                            2s_contested, 3s_contested, contested_shots, off_box_outs,
                            def_box_outs, box_outs)
                            values ({0}, "{1}", "{2}", "{3}", {4}, {5}, {6}, {7}, {8},
                            {9}, {10}, {11}, {12}, {13}, {14}, {15}, {16})
                            """.format(nbaID, player, formattedDate, mins, screen_ast,
                                screen_ast_pts, deflections, off_loose_balls, def_loose_balls,
                                loose_balls, charges_drawn, two_contests, three_contests,
                                shot_contests, off_boxouts, def_boxouts, boxouts  
                            )
                    print(query)
                    #cursor.execute(query)
            break
    pdb.set_trace()
    #cnx.commit()
    return

def getMatchups (driver, cnx, cursor, date, socket=None):
    # table layout is different form matchups..... :S
    select = Select(driver.find_element_by_name('splits'))
    print(date)
    formattedDate = datetime.date(int(date[-4:]), int(date[3:5]), int(date[:2]))
    print (formattedDate)
    for option in select.options:
        if 'Matchups' == option.text:
            select.select_by_value('matchups')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'Pagination_button__1MPZe')))
            pagnation = driver.find_elements_by_class_name('Pagination_button__1MPZe')
            while (1):
                table = driver.find_element_by_tag_name('tbody')
                tableRows = table.find_elements_by_tag_name('tr')
                for row in range(len(tableRows)):
                    offPlayer = tableRows[row].find_elements_by_tag_name('td')[0].text
                    offnbaID = tableRows[row].find_elements_by_tag('td')[0].find_elements_by_tag('a').get_attribute('href')
                    offTeam = tableRows[row].find_elements_by_tag_name('td')[1].text
                    defPlayer = tableRows[row].find_elements_by_tag_name('td')[2].text
                    defnbaID = tableRows[row].find_elements_by_tag('td')[2].find_elements_by_tag('a').get_attribute('href')
                    defTeam = tableRows[row].find_elements_by_tag_name('td')[3].text
                    mins = tableRows[row].find_elements_by_tag_name('td')[4].text
                    partial_poss = tableRows[row].find_elements_by_tag_name('td')[5].text
                    per_def_time = tableRows[row].find_elements_by_tag_name('td')[6].text
                    per_off_time = tableRows[row].find_elements_by_tag_name('td')[7].text
                    per_both_time = tableRows[row].find_elements_by_tag_name('td')[8].text
                    player_pts = tableRows[row].find_elements_by_tag_name('td')[9].text
                    team_pts = tableRows[row].find_elements_by_tag_name('td')[10].text
                    ast = tableRows[row].find_elements_by_tag_name('td')[11].text
                    tov = tableRows[row].find_elements_by_tag_name('td')[12].text
                    blk = tableRows[row].find_elements_by_tag_name('td')[13].text
                    fgm = tableRows[row].find_elements_by_tag_name('td')[14].text
                    fga = tableRows[row].find_elements_by_tag_name('td')[15].text
                    fgPer = tableRows[row].find_elements_by_tag_name('td')[16].text
                    threefgm = tableRows[row].find_elements_by_tag_name('td')[17].text
                    threefga = tableRows[row].find_elements_by_tag_name('td')[18].text
                    threefgPer = tableRows[row].find_elements_by_tag_name('td')[19].text
                    ftm = tableRows[row].find_elements_by_tag_name('td')[20].text
                    fta = tableRows[row].find_elements_by_tag_name('td')[21].text
                    sfl = tableRows[row].find_elements_by_tag_name('td')[22].text
                    query = """
                            insert into matchups
                            ("off_player", "team1", "def_player", "team2", "mins", 
                            partial_poss, per_def_time, per_off_time, per_time_both_on,
                            player_pts, team_pts, ast, tov, blk, fgm, fga, fgPer, 
                            3fgm, 3fga, 3fgPer, ftm, fta, sfl, 
                            off_player_nbaID, def_player_nbaID, "date")
                            """.format(
                                offPlayer, offTeam, defPlayer, defTeam, mins,
                                partial_poss, per_def_time, per_off_time, per_both_time,
                                player_pts, team_pts, ast, tov, blk, fgm, fga, fgPer,
                                threefgm, threefga, threefgPer, ftm, fta, sfl,
                                offnbaID, defnbaID, formattedDate
                            )
                    print(query)
                    #cursor.execute(query)

                if pagnation[1].is_enabled():
                    pagnation[1].click()
                    table = None
                else :
                    break
    
    #cnx.commit()
    return


def findMaxDate(cursor):
    query = "select max(date) from hustle"
    cursor.execute(query)
    return cursor.fetchone()