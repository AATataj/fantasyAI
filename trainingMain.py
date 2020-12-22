import mysql.connector
from team import team
from league import league
from matchup import matchup
from rotoworldScraper import updateRoto
from linearRegression import linReg
from availSentiment import trainSentimentAvail, trainSentimentTrades
from compileRosters import setRostersRAM
from compileRosters import updateRostersRAM
from createAvailabilitySet import createAvailTable, addGames, correctForTrades, correctAlecBurks, getLatestArticles
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

#train(cnx)
#linReg(cnx)
#createSentimentData(cnx)
#createAvailTable(2019, cnx)
#addGames(cnx)
#print(correctForTrades(cnx))
#print(correctAlecBurks(cnx))
#print(getLatestArticles(cnx))
print(trainSentimentTrades(cnx))
#playerList = setRostersRAM(2019, cnx)

#playerList = updateRostersRAM(playerList, '2020-02-01', cnx)
 

cnx.close()