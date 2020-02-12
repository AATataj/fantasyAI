import time, datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
from datetime import date
import unidecode
import pdb


def scrapeScores(cnx):
    cursor = cnx.cursor()
    query = "select max(date) from boxscores"
    cursor.execute(query)
    maxDate = cursor.fetchone()

    print (str(type(maxDate)))
    if maxDate[0].month > 9:
        sendDate = maxDate[0].year 
    else: 
        sendDate = maxDate[0].year -1
    if date.today().month > 9 :
        currYear = date.today().year
    else :
        currYear = date.today().year -1

    #early termination if already up to date
    #if maxDate[0] == date.today():
         #return

    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)
    driver.get("https://www.basketball-reference.com/play-index/pgl_finder.cgi")
    
    minYearSelect = driver.find_element_by_id("year_min")
    maxYearSelect = driver.find_element_by_id("year_max")
    orderBySelect = driver.find_element_by_id("order_by")
    submit = driver.find_element_by_xpath("//*[@value = 'Get Results']")

    minYearSelect.send_keys(sendDate)
    maxYearSelect.send_keys(currYear)
    orderBySelect.send_keys("date_game")
    submit.submit()

    dateFlag = False
    while (driver.find_element_by_link_text("Next page")):    
        time.sleep(3)
        headers = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/thead/tr/th")
        rows = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/tbody/tr")
        row = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/tbody/tr/td")
        if dateFlag :
            break
        for rowElem in rows:
            linebuffer =[]
            cols = rowElem.find_elements_by_xpath("td")
            colIndex = 1
            for cell in cols:
                linebuffer.append(cell.text)
                colIndex += 1
            """
                index key for linebuffer:
                0 : name        1 : age     2 : position    3 : date    4 : team    5 : homeAway
                6 : opponent    7 : result  8 : started     9 : minutes 10 : fgm    11 : fga
                12 : fgPer      13 : 2fgm   14 : 2fga       15 : 2fgPer 16 : 3fgm   17 : 3fga
                18 : 3fgPer     19 : ftm    20 : fta        21 : ftPer  22 : orb    23 : drb
                24 : trb        25 : ast    26 : stl        27 : blk    28 : tov    29 : pf
                30 : pts        31 : gmsc
            """
            if linebuffer != []:
                # cuz it can never be easy thanks to bball reference 
                # deciding to do something dumb after 40 years of data
                if unidecode.unidecode(linebuffer[0]) == 'Jokob Poltl':
                    linebuffer[0] = 'Jokob Poeltl'
                query = """
                        insert into boxscores2 
                        (name, age, position, date, team, homeAway, opponent, result, started, minutes,
                        fgm, fga, fgPer, 2fgm, 2fga, 2fgPer, 3fgm, 3fga, 3fgPer, ftm, fta, ftPer,
                        orb, drb, trb, ast, stl, blk, tov, pf, pts)
                        values ("{0}", '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', {9}, {10},
                        {11}, {12}, {13}, {14}, {15}, {16}, {17}, {18}, {19}, {20}, {21}, {22},
                        {23}, {24}, {25}, {26}, {27}, {28}, {29}, {30})
                        """.format(unidecode.unidecode(linebuffer[0]), 
                        linebuffer[1], linebuffer[2], datetime.datetime.strptime(linebuffer[3], '%Y-%m-%d'),  
                        ## team, h/a, opp, result, started
                        linebuffer[4], linebuffer[5], linebuffer[6], linebuffer[7], linebuffer[8], 
                        ## mins
                        int(linebuffer[9]), 
                        ## fgs 
                        int(linebuffer[10]),  int(linebuffer[11]), float(linebuffer[12] if linebuffer[12] != '' else 0.0),  
                        ## 2fgs
                        int(linebuffer[13]), int(linebuffer[14]), float(linebuffer[15] if linebuffer[15] != '' else 0.0),
                        ## 3fgs
                        int(linebuffer[16]), int(linebuffer[17]), float(linebuffer[18] if linebuffer[18] != '' else 0.0),
                        ## fts
                        int(linebuffer[19]), int(linebuffer[20]), float(linebuffer[21] if linebuffer[21] != '' else 0.0), 
                        ## rebs
                        int(linebuffer[22]), int(linebuffer[23]), int(linebuffer[24]), 
                        ## ast, stl, blk
                        int(linebuffer[25]), int(linebuffer[26]), int(linebuffer[27]), 
                        ## tov, pf, pts
                        int(linebuffer[28]), int(linebuffer[29]), int(linebuffer[30]), 
                        ## gmsc
                        float(linebuffer[31]))
            
            print(linebuffer)
            if linebuffer != [] : 
                if (datetime.datetime.strptime(linebuffer[3], '%Y-%m-%d') 
                    < datetime.datetime(maxDate[0].year, maxDate[0].month, maxDate[0].day)) :
                    dateFlag = True
                    break
                cursor.execute(query)
                cnx.commit()
        next_page = driver.find_element_by_link_text("Next page")
        driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
        next_page.click()
        print("--- NEXT PAGE ---")
        

    updatePlayerIDs(cnx)
    query = """
            select count(*) from boxscores2 where playerID is null
            """
    cursor.execute(query)
    idMissingCount = cursor.fetchone()
    ## for new players with no entry:
    if idMissingCount[0] != 0 :
        query = """
                insert into playerHashes (name, dob) 
                select distinct name, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), 
                interval cast(substr(age, 4,3) as signed) day) as dob from boxscores2 group by name, dob;
                """
        cursor.execute(query)
        cnx.commit()
        updatePlayerIDs(cnx)
    
    ## insert new boxscores into live table
    query = """
            insert into boxscores select * from boxscores2
            """ 
    cursor.execute(query)
    cnx.commit()

    ##purge boxscores2 table
    query = """
            delete from boxscores2
            """
    cursor.execute(query)
    cnx.commit(0)

   
    driver.quit()
    return
def updatePlayerIDs(cnx):
    cursor = cnx.cursor()
    ## append playerID to new table : 
    query = """
            update boxscores2
            inner join playerHashes
            on playerHashes.name = boxscores2.name 
            set boxscores2.playerID = playerHashes.playerID
            where 
            datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =0 or
            datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =1 or
            datediff(playerHashes.dob, date_sub(date_sub(date, interval cast(substr(age, 1,2) as signed) year), interval cast(substr(age, 4,3) as signed) day)) =-1
            """
    cursor.execute(query)
    cnx.commit()
    return