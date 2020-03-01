import mysql.connector
import datetime
import pdb

import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

## this file is meant to be an example of utilizing 
## pandas to calculate my day-by-day feature vectors via pandas.dataFrame()
## I will not be listing all the calculated features here as it will be 
## awfully redundant, as well as giving away all my best ideas publicly

def addNewFeature(featureName,featureQuery, cnx):
        ### IMPORTANT INFO ###
        ### This function is set up so that a new feature is defaulted as a 
        ### floating point value (decimal (7,4) in SQL) as a new column
        ### if the datatype is different, we need to change the 
        ### alter table query below as well (line 58)
       
        ## connection stuff
        cursor = cnx.cursor()
        engine = create_engine("mysql://slick:muresan44@localhost/nba")
        con = engine.connect()
        
        ## necessary data for calculated features
        #query = """
                #select name, playerID, date,
                #fgPer, ftPer, 3fgm, pts, trb, ast, stl, blk, tov   
                #from boxscores limit 20
                #"""
        query = """
                select name, date, playerID from inputvectors
                """
        dataFrame = pd.read_sql_query(query, cnx)
        ## cast date column to a datetime object
        dataFrame['date'] = pd.to_datetime(dataFrame['date'], format = '%Y-%m-%d')

        #dataFrame = pd.read_sql_query(query, cnx)
        newFeature = pd.Series()
        
        
        ## run the queries to calculate the new feature set
        for row in range(len(dataFrame)):
                query = featureQuery.format(dataFrame.loc[row, 'playerID'], dataFrame.loc[row, 'date'])
                data = pd.read_sql_query(query, cnx)
                ## append calculated feature value to new feature series
                newFeature = newFeature.append(data.loc[0], ignore_index=True)
        
        ## remove me after testing!!
        #cursor.execute("alter table inputvectors drop column {0}}".format(featureName))
        ## /remove
        
        
        query = """
                alter table inputvectors
                add column {0} decimal(7,4)
                """.format(featureName)
        cursor.execute(query)       
        
        
        query = ''
        for i in range(len(newFeature.array)):
                query += """
                        update inputvectors
                        set {0} = {1}
                        where `index` = {2};
                        """.format(featureName, newFeature[i], i+1)
        
        ## why do I need a loop in an execute multi=True call?
        ## it's stupid, that's why
        for result in cursor.execute(query, multi=True):
                pass
        cnx.commit()

        query = """
                insert into featuresList (feature)
                values ("{0}")
                """.format(featureQuery)
        cursor.execute(query)
        cnx.commit()