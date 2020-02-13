import mysql.connector
from team import team
from league import league
from matchup import matchup
from rotoworldScraper import updateRoto
from liveBoxScrape import scrapeScores
import datetime
import pdb 
import unidecode

import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

"""mysql-python-connector"""
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor(dictionary=True)

print("****************")
print("****Test Bed****")
print("****************")

print(unidecode.unidecode('Luka Dončić'))
#updateRoto(cnx)
#scrapeScores(cnx)

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