import time, datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector
from datetime import date
import csv

import pdb

def bballScraper(cnx):
    cursor = cnx.cursor()
    query = "select max(date) from boxscores"
    cursor.execute(query)
    maxDate = cursor.fetchone()

    print (str(type(maxDate)))
    print (maxDate[0].month)

    driver = webdriver.Chrome('/usr/bin/chromedriver')
    chrome_opts = Options()
    chrome_opts.add_argument("--headless")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=chrome_opts)
    driver.get("https://www.basketball-reference.com/play-index/pgl_finder.cgi")
    
    minYearSelect = driver.find_element_by_id("year_min")
    maxYearSelect = driver.find_element_by_id("year_max")
    orderBySelect = driver.find_element_by_id("order_by")
    submit = driver.find_element_by_xpath("//*[@value = 'Get Results']")

    minYearSelect.send_keys(maxDate[0].year - 1)
    maxYearSelect.send_keys(date.today().year - 1)
    orderBySelect.send_keys("date_game")
    submit.submit()
    with open('bballref.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        while (driver.find_element_by_link_text("Next page")):    
            time.sleep(3)
            headers = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/thead/tr/th")
            rows = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/tbody/tr")
            row = driver.find_elements_by_xpath("//table[@class = 'sortable stats_table now_sortable sliding_cols']/tbody/tr/td")

            linebuffer =[]
            rowIndex = 1
            for rowElem in rows:
                cols = rowElem.find_elements_by_xpath("td")
                colIndex = 1
                for cell in cols:
                    linebuffer.append(cell.text)
                    colIndex += 1
                print(linebuffer)
                writer.writerow(linebuffer)
                file.flush()
                linebuffer = []
                rowIndex += 1
            next_page = driver.find_element_by_link_text("Next page")
            driver.execute_script("arguments[0].scrollIntoView(true);", next_page)
            next_page.click()
            print("--- NEXT PAGE ---")
            

    driver.quit()
