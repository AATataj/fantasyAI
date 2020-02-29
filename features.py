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
        ### alter table query below as well
       
        ## connection stuff
        cursor = cnx.cursor()
        engine = create_engine("mysql://slick:muresan44@localhost/nba")
        con = engine.connect()
        
        ## necessary data for calculated features
        query = """
                select name, playerID, date,
                fgPer, ftPer, 3fgm, pts, trb, ast, stl, blk, tov   
                from boxscores limit 20
                """
        dataFrame = pd.read_sql_query(query, cnx)
        newFeature = pd.Series()
        
        ## cast date column to a datetime object
        dataFrame['date'] = pd.to_datetime(dataFrame['date'], format = '%Y-%m-%d')
        
        ## run the queries to calculate the new feature set
        for row in range(len(dataFrame)):
                query = featureQuery.format(dataFrame.loc[row, 'playerID'], dataFrame.loc[row, 'date'])
                data = pd.read_sql_query(query, cnx)
                ## append calculated feature value to new feature series
                newFeature = newFeature.append(data.loc[0], ignore_index=True)
        
        ## remove me after testing!!
        cursor.execute("alter table inputvectors drop column ptsAvg7Days")
        ## /remove
        
        colNames = []
        colTypes = []
        for col in dataFrame.columns:
                colNames.append(col)
                if dataFrame[col].dtype == 'object':
                        colTypes.append('varchar(150)')
                if dataFrame[col].dtype == 'int64':
                        colTypes.append('int')
                if dataFrame[col].dtype == 'datetime64[ns]':
                        colTypes.append('date')
                if dataFrame[col].dtype == 'float64':
                        colTypes.append('decimal(7,4)')

        # create the table inputvectors based on the newly compiled dataframe
        # will be removed after the full thing is created        
        query = """
                        create table inputvectors ( 
                        `index` int 
                        not null auto_increment,      
                        """
        for i in range(len(colNames)):
                query += colNames[i] + " " + colTypes[i] + ',' 
        query = query[:-1]
        query += ', primary key (`index`))'
        cursor.execute(query)
        # /remove
        
        ## inputvectors input, tried to remove the need to load sqlAlchemy
        ## library, but the to_sql function seems to play favorites
        dataFrame.to_sql(name='inputvectors',index=False, con=con, if_exists='append')
        
        query = """
                alter table inputvectors
                add column {0} decimal(7,4)
                """.format(featureName)
        cursor.execute(query)
        query = """
                select name, date, playerID from inputvectors
                """
        dataFrame = pd.read_sql_query(query, cnx)

        
        
        print(newFeature.array)
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