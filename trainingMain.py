import mysql.connector
from team import team
from league import league
from matchup import matchup
from rotoworldScraper import updateRoto
from liveBoxScrape import scrapeScores
from liveBoxScrape import updatePlayerIDs
from features import addNewFeature
from linearRegression import linReg
from sentiment import createSentimentData
from compileRosters import setRostersRAM
from compileRosters import updateRostersRAM

import pdb 
import unidecode

import pathlib
import pandas as pd

"""mysql-python-connector"""
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor(dictionary=True)

print("****************")
print("****Test Bed****")
print("****************")

#updateRoto(cnx)
#scrapeScores(cnx)

featureQuery = """
                select AVG(pts)
                from boxscores
                where playerID = {0}
                and date < '{1}'
                """
#addNewFeature('trbAvgCareer', featureQuery, cnx)

#train(cnx)
#linReg(cnx)
createSentimentData(cnx)

#playerList = setRostersRAM(2019, cnx)

#playerList = updateRostersRAM(playerList, '2020-02-01', cnx)
 

"""teamname=None
testLeague = league(15,5,3,2012,"Test League", cnx)
for i in range(2):
    teamname = "team{0}".format(i) 
    testteam = team(15,teamname,3,cnx) 
    testLeague.mockDraft(testteam)
    testLeague.addTeam(testteam)
    for player in testLeague.teams[i].roster:
        testLeague.freeAgents.remove(player)
testLeague.schedule = testLeague.roundRobin(3)


for team in testLeague.teams:
    print(team.owner + " : ")
    print(team.roster)
    print(team.lineup)

print(testLeague.seasonStart)
print(testLeague.seasonEnd)
for day in range(7):
    testLeague.rollDay()
    for team in testLeague.teams:
        print (team.owner + " " + str(team.weeklyTotals))
        print (team.owner + " " + str(team.record))
"""
cnx.close()