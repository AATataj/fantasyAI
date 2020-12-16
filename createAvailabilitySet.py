# create availability dataset
# create an availability table containing:
# player name, id, current team, date and :
# latest article and article title given the latest game date of current team

import mysql.connector
import datetime
import pandas as pd
import pdb

# strategy :
# 1.  take every unique player based on first appearance in boxscores, add those players to the table
# 2.  back fill and forward fill every player that appears in the table for those team's games.
# 3.  find all instances from rotoworld table where player's last entry's team != current entry team
# 4.  remove all entries from table where the team changes mid-season and forward fill games for the new team

def createAvail(startYear, cnx):
    cursor = cnx.cursor()
    octMin = datetime.date(startYear, 10, 1)

    
    print (octMin)
    return "success!" 
