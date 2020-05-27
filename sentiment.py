# sentiment.py
import pdb

import numpy as np 
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print (tf.__version__)

import tensorflow_docs as tfdocs
import tensorflow_docs.plots

##
## This is gonna be the sentiment analysis of player availability
## Starting tomorrow this is the next focus.
## Afterward, we'll work on quickening up features processing
## and look into creating a k8s cluster here at home
## :D :D :D
##

#   Strategy:
#   gather games :
#   select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
#   gather playernotes:
#   select * from rotoworld where playerID is not null;
#   stitch together by taking max(date) of rotoworld, and appending it to date of each applicable game
#   how to determine dnp-cds vs dnp-inj?

def sentiment(cnx):
    
    cursor = cnx.cursor()
    ## gather nba games schedule:
    query = """
            select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
            """
    schedule = pd.read_sql_query(query,cnx)
    schedule.rename(columns={'team':'away', 'opponent' : 'home'}, inplace=True)
    del schedule['homeAway']

    print(schedule.head())

    query = """
            select * from rotoworld where playerID is not null;
            """
    playerNotes = pd.read_sql_query(query,cnx)

    print(playerNotes.head())


def teamMap(full):
    if 'DETROIT PISTONS' in full:
        out = 'DET'
    elif 'OKLAHOMA CITY THUNDER' in full:
        out = 'OKC'
    elif 'NEW ORLEANS PELICANS' in full:
        out = 'NOP'
    elif 'SAN ANTONIO SPURS' in full:
        out = 'SAS'
    elif 'NEW YORK KNICKS' in full:
        out = 'NYK'
    elif 'ATLANTA HAWKS' in full:
        out = 'ATL'
    elif 'BROOKLYN NETS' in full:
        out = 'BRK'
    elif 'BOSTON CELTICS' in full:
        out = 'BOS'
    elif 'INDIANA PACERS' in full:
        out = 'IND'
    elif 'SACRAMENTO KINGS' in full:
        out = 'SAC'
    elif 'PORTLAND TRAIL BLAZERS' in full:
        out = 'POR'
    elif 'UTAH JAZZ' in full:
        out = 'UTA'
    elif 'PHOENIX SUNS' in full:
        out = 'PHX'
    elif 'DENVER NUGGETS' in full:
        out = 'DEN'
    elif 'MINNESOTA TIMBERWOLVES' in full:
        out = 'MIN'
    elif 'LOS ANGELES LAKERS' in full:
        out = 'LAL'
    elif 'LOS ANGELES CLIPPERS' in full:
        out = 'LAC'
    elif 'MEMPHIS GRIZZLIES' in full:
        out = 'MEM'
    elif 'MIAMI HEAT' in full:
        out = 'MIA'
    elif 'TORONTO RAPTORS' in full:
        out = 'TOR'
    elif 'HOUSTON ROCKETS' in full:
        out = 'HOU'
    elif 'CLEVELAND CAVALIERS' in full:
        out = 'CLE'
    elif 'PHILADELPHIA 76ERS' in full:
        out = 'PHI'
    elif 'MILWAUKEE BUCKS' in full:
        out = 'MIL'
    elif 'CHARLOTTE HORNETS' in full:
        out = 'CHO'
    elif 'CHICAGO BULLS' in full:
        out = 'CHI'
    elif 'DALLAS MAVERICKS' in full:
        out = 'DAL'
    elif 'GOLDEN STATE WARRIORS' in full:
        out = 'GSW'
    elif 'ORLANDO MAGIC' in full:
        out = 'ORL'
    elif 'WASHINGTON WIZARDS' in full:
        out = 'WAS'
    return out