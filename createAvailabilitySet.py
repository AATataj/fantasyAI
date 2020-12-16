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

def createAvailTable(startYear, cnx):
    cursor = cnx.cursor()
    octMin = datetime.date(startYear, 10, 1)

    query = """
            select * from rotoworld as r2
            inner join 
                (select name, nbaID, playerID, min(date) as date 
                from rotoworld 
                group by name, nbaID, playerID) as r1
            on r2.playerID = r1.playerID and r2.date = r1.date;
            """
    cursor.execute(query)
    results = cursor.fetchall()
    
    for result in results:
        team = teamMap(result[1])
        query = """
                insert into availData 
                (name, team, recentTitle, recentContent, reportDate, playerID, nbaID)
                values ("{0}","{1}","{2}","{3}","{4}",{5},{6} )
                """.format(result[0], 
                           team, 
                           result[2].replace('"', "'"), 
                           result[3].replace('"', "'"), 
                           result[4], 
                           result[5], 
                           result[6])    
        try :
            cursor.execute(query)
        except :
            print(result[0])
            print(team)
            print(result[2])
            print(result[3])
            print(result[4])
            print(result[5])
            print(result[6])
    cnx.commit()
    return "success!" 

def teamMap(posTeam):

    ## maps teamPos data to boxscore team abbreviations
    out = ""
    if 'DETROIT PISTONS' in posTeam:
        out = 'DET'
    elif 'OKLAHOMA CITY THUNDER' in posTeam:
        out = 'OKC'
    elif 'NEW ORLEANS PELICANS' in posTeam:
        out = 'NOP'
    elif 'SAN ANTONIO SPURS' in posTeam:
        out = 'SAS'
    elif 'NEW YORK KNICKS' in posTeam:
        out = 'NYK'
    elif 'ATLANTA HAWKS' in posTeam:
        out = 'ATL'
    elif 'BROOKLYN NETS' in posTeam:
        out = 'BRK'
    elif 'BOSTON CELTICS' in posTeam:
        out = 'BOS'
    elif 'INDIANA PACERS' in posTeam:
        out = 'IND'
    elif 'SACRAMENTO KINGS' in posTeam:
        out = 'SAC'
    elif 'PORTLAND TRAIL BLAZERS' in posTeam:
        out = 'POR'
    elif 'UTAH JAZZ' in posTeam:
        out = 'UTA'
    elif 'PHOENIX SUNS' in posTeam:
        out = 'PHX'
    elif 'DENVER NUGGETS' in posTeam:
        out = 'DEN'
    elif 'MINNESOTA TIMBERWOLVES' in posTeam:
        out = 'MIN'
    elif 'LOS ANGELES LAKERS' in posTeam:
        out = 'LAL'
    elif 'LOS ANGELES CLIPPERS' in posTeam:
        out = 'LAC'
    elif 'MEMPHIS GRIZZLIES' in posTeam:
        out = 'MEM'
    elif 'MIAMI HEAT' in posTeam:
        out = 'MIA'
    elif 'TORONTO RAPTORS' in posTeam:
        out = 'TOR'
    elif 'HOUSTON ROCKETS' in posTeam:
        out = 'HOU'
    elif 'CLEVELAND CAVALIERS' in posTeam:
        out = 'CLE'
    elif 'PHILADELPHIA 76ERS' in posTeam:
        out = 'PHI'
    elif 'MILWAUKEE BUCKS' in posTeam:
        out = 'MIL'
    elif 'CHARLOTTE HORNETS' in posTeam:
        out = 'CHO'
    elif 'CHICAGO BULLS' in posTeam:
        out = 'CHI'
    elif 'DALLAS MAVERICKS' in posTeam:
        out = 'DAL'
    elif 'GOLDEN STATE WARRIORS' in posTeam:
        out = 'GSW'
    elif 'ORLANDO MAGIC' in posTeam:
        out = 'ORL'
    elif 'WASHINGTON WIZARDS' in posTeam:
        out = 'WAS'
    return out