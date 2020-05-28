#compile rosters
# this file is going to manage each team's roster for a given season
#

import mysql.connector
import datetime
import pandas as pd


def setRosters(startYear, cnx):
    ## this one will append any new players who played a game for a team
    ## during the first month of a season to that team's roster.
    cursor = cnx.cursor()

    ## initialization
    octMin = datetime.datetime(startYear, 10, 1)
    query = """
            select min(date) from boxscores where date > '{0}';
            """.format(octMin)
    cursor.execute(query)
    start = cursor.fetchone()


    teams = ['MIL', 'TOR', 'BOS', 'MIA', 'IND', 'PHI', 'BRK', 'ORL', 
            'WAS', 'CHO', 'CHI', 'NYK', 'DET', 'ATL', 'CLE', 'LAL',
            'LAC', 'DEN', 'UTA', 'OKC', 'HOU', 'DAL', 'MEM', 'POR',
            'NOP', 'SAC', 'SAS', 'PHO', 'MIN', 'GSW']
    
    start = start[0]
    end = start + datetime.timedelta(days=30)  
    
    query = """
            select distinct(playerID), name, team from boxscores where date > '{0}' and date < '{1}';
            """.format(start,end)
    ## return list of players who played in first 30 days
    playerList = pd.read_sql_query(query, cnx)

    query = """"""
    for team in teams:
            query+="create table {0}-{1}-{2} (name varchar(100), playerID int(11));\n".format(
                    team,str(startYear), str(startYear+1))
    print (query)

    for i in range (len(playerList.index)):
        print (playerList.iloc[i].loc['name'], playerList.iloc[i].loc['team'], playerList.iloc[i].loc['playerID'])
        if playerList.iloc[i].loc['team'] == 'MIL':
        if playerList.iloc[i].loc['team'] == 'TOR':
        if playerList.iloc[i].loc['team'] == 'BOS':
        if playerList.iloc[i].loc['team'] == 'MIA':
        if playerList.iloc[i].loc['team'] == 'IND':
        if playerList.iloc[i].loc['team'] == 'PHI':
        if playerList.iloc[i].loc['team'] == 'BRK':
        if playerList.iloc[i].loc['team'] == 'ORL':
        if playerList.iloc[i].loc['team'] == 'WAS':
        if playerList.iloc[i].loc['team'] == 'CHO':
        if playerList.iloc[i].loc['team'] == 'CHI':
        if playerList.iloc[i].loc['team'] == 'NYK':
        if playerList.iloc[i].loc['team'] == 'DET':
        if playerList.iloc[i].loc['team'] == 'ATL':
        if playerList.iloc[i].loc['team'] == 'CLE':
        if playerList.iloc[i].loc['team'] == 'LAL':
        if playerList.iloc[i].loc['team'] == 'LAC':
        if playerList.iloc[i].loc['team'] == 'DEN':
        if playerList.iloc[i].loc['team'] == 'UTA':
        if playerList.iloc[i].loc['team'] == 'OKC':
        if playerList.iloc[i].loc['team'] == 'HOU':
        if playerList.iloc[i].loc['team'] == 'DAL':
        if playerList.iloc[i].loc['team'] == 'MEM':
        if playerList.iloc[i].loc['team'] == 'POR':
        if playerList.iloc[i].loc['team'] == 'NOP':
        if playerList.iloc[i].loc['team'] == 'SAC':
        if playerList.iloc[i].loc['team'] == 'SAS':
        if playerList.iloc[i].loc['team'] == 'PHO':
        if playerList.iloc[i].loc['team'] == 'MIN':
        if playerList.iloc[i].loc['team'] == 'GSW':
    