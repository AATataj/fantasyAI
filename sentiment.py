# sentiment.py
import pdb

import numpy as np 
import pandas as pd
import mysql.connector
from compileRosters import setRostersRAM
from compileRosters import updateRostersRAM

import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


import tensorflow_docs as tfdocs
import tensorflow_docs.plots

##
## This is gonna be the sentiment analysis of player availability
## Starting tomorrow this is the next focus.
##

#   Strategy:
#   gather games :
#   select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
#   gather playernotes:
#   select * from rotoworld where playerID is not null;
#   stitch together by taking max(date) of rotoworld, and appending it to date of each applicable game
#   how to determine dnp-cds vs dnp-inj?

def createSentimentData(cnx):
    
    cursor = cnx.cursor()
    startYear = 2019
    ## gather nba games schedule 2019-2020:
    query = """
            select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
            """
    schedule = pd.read_sql_query(query,cnx)
    schedule.rename(columns={'team':'away', 'opponent' : 'home'}, inplace=True)
    del schedule['homeAway']
    print(schedule.head())


    # get a list of all players who appeared in all games over the course of the 2019-2020 season
    playerList = setRostersRAM(startYear,cnx)
    schedule = schedule.sort_values(by=['date'])
    sentimentData = pd.DataFrame(columns= ['playerID', 'name', 'date', 'home', 'away', 'recentTitle', 'recentContent', 'played'])
    for x in range(len(schedule)):
        print (schedule.iloc[x]['home'] + " vs " + schedule.iloc[x]['away'] + ' on ' + str(schedule.iloc[x]['date']))
        currentDate = schedule.iloc[x]['date']
        # update the rosters on every given day to check for trades, swaps, etc
        if schedule.iloc[x]['date'] != currentDate:
            updateRostersRAM(playerList,schedule.iloc[x]['date'], cnx)
        ## for each player who is on a team who plays on the date, we need to pull their last
        for y in range (len(playerList)):
            if playerList.iloc[y]['team'] == schedule.iloc[x]['home'] or playerList.iloc[y]['team'] == schedule.iloc[x]['away']:
                ## select the max date < game date for a rotoworld entry for the given player
                ## then append this to a features dataframe
                query = """
                        SELECT max(date), name, playerID, title, content 
                        FROM rotoworld 
                        WHERE date < '{0}' and playerID = {1}
                        GROUP BY playerID, name, title, content
                        LIMIT 1;
                        """.format(currentDate, playerList.iloc[y]['playerID'])
                result = pd.read_sql_query(query,cnx)
                query = """
                        SELECT name from boxscores 
                        WHERE playerID = {0} and date = '{1}'
                        """.format(playerList.iloc[y]['playerID'], currentDate)
                answer = pd.read_sql_query(query,cnx)
                if not answer.empty:
                    played = 1
                else:
                    played = 0
                if not result.empty:
                    sentimentData = sentimentData.append({'playerID' : playerList.iloc[y]['playerID'],
                                      'name' : playerList.iloc[y]['name'],
                                      'date' : currentDate,
                                      'home' : schedule.iloc[x]['home'],
                                      'away' : schedule.iloc[x]['away'],
                                      'recentTitle' : result.iloc[0]['title'],
                                      'recentContent' : result.iloc[0]['content'],
                                      'played' : played
                                    },ignore_index=True)
                else : 
                    sentimentData = sentimentData.append({'playerID' : playerList.iloc[y]['playerID'],
                                      'name' : playerList.iloc[y]['name'],
                                      'date' : currentDate,
                                      'home' : schedule.iloc[x]['home'],
                                      'away' : schedule.iloc[x]['away'],
                                      'played' : played
                    },ignore_index=True)
         
    
    print (sentimentData.head())
    # insert into availabilityData table
    for row in range(len(sentimentData)):
        if(pd.isna(sentimentData.iloc[row]['recentTitle'])):
            sentimentData.at[row, 'recentTitle'] = ""
        if(pd.isna(sentimentData.iloc[row]['recentContent'])):
            sentimentData.at[row, 'recentContent'] = ""
        query = """
                insert into availabilityData values ({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", {7});
                """.format(
                        sentimentData.iloc[row]['playerID'],
                        sentimentData.iloc[row]['name'],
                        sentimentData.iloc[row]['date'],
                        sentimentData.iloc[row]['home'],
                        sentimentData.iloc[row]['away'],
                        sentimentData.iloc[row]['recentTitle'].replace('"', '\\"'),
                        sentimentData.iloc[row]['recentContent'].replace('"', '\\"'),
                        sentimentData.iloc[row]['played'] 
                        )
        cursor.execute(query)
        
    cnx.commit()
    

    """query = 
            select * from rotoworld where playerID is not null;
            """
    #playerNotes = pd.read_sql_query(query,cnx)
    #playerNotes.rename(columns={'date':'reportDate'}, inplace=True)
    #print(playerNotes.head())

def trainSentimentTrades(cnx):
    # train the algo for detecting player movement articles
    
    return

def trainSentimentAvail(cnx):
    # train the algo for player availability
    
    return