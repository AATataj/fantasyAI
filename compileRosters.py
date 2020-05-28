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
    
    ## create list of rosters
    rosters = []
    for team in teams:
            rosters.append({'team':team, 'roster':[]})
    #print (rosters)

    for i in range (len(playerList.index)):
        #print (playerList.iloc[i].loc['name'], playerList.iloc[i].loc['team'], playerList.iloc[i].loc['playerID'])
        if playerList.iloc[i].loc['team'] == 'MIL':
                rosters[0]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'TOR':
                rosters[1]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'BOS':
                rosters[2]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'MIA':
                rosters[3]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'IND':
                rosters[4]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'PHI':
                rosters[5]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'BRK':
                rosters[6]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'ORL':
                rosters[7]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'WAS':
                rosters[8]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'CHO':
                rosters[9]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'CHI':
                rosters[10]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'NYK':
                rosters[11]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'DET':
                rosters[12]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'ATL':
                rosters[13]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'CLE':
                rosters[14]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'LAL':
                rosters[15]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'LAC':
                rosters[16]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'DEN':
                rosters[17]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'UTA':
                rosters[18]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'OKC':
                rosters[19]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'HOU':
                rosters[20]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'DAL':
                rosters[21]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'MEM':
                rosters[22]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'POR':
                rosters[23]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'NOP':
                rosters[24]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'SAC':
                rosters[25]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'SAS':
                rosters[26]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'PHO':
                rosters[27]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'MIN':
                rosters[28]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        if playerList.iloc[i].loc['team'] == 'GSW':
                rosters[29]['roster'].append((playerList.iloc[i].loc['name'],playerList.iloc[i].loc['playerID']))
        
    