import mysql.connector
import datetime
import pdb

import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

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
        start_time = time.time()
        
        query = """
                select name, date, playerID from inputvectors
                """
        dataFrame = pd.read_sql_query(query, cnx)
        ## cast date column to a datetime object
        dataFrame['date'] = pd.to_datetime(dataFrame['date'], format = '%Y-%m-%d')

        dataframe_end = time.time() - start_time
        print('dataframe generation completed.....time elapsed : {0}'.format(dataframe_end))
        #dataFrame = pd.read_sql_query(query, cnx)
        newFeature = pd.Series()
        
        features_start = time.time()
        ## run the queries to calculate the new feature set
        if 'Season' in featureName: 
                for row in range(len(dataFrame)):
                        query = featureQuery.format\
                                        (dataFrame.loc[row, 'playerID'], dataFrame.loc[row, 'date'], \
                                        datetime.date(dataFrame.loc[row, 'date'].year,10,1) \
                                        if dataFrame.loc[row, 'date'].month>9 \
                                        else datetime.date(dataFrame.loc[row, 'date'].year-1,10,1))
                        data = pd.read_sql_query(query, cnx)
                        ## append calculated feature value to new feature series
                        newFeature = newFeature.append(data.loc[0], ignore_index=True)
        else:
                for row in range(len(dataFrame)):
                        query = featureQuery.format(dataFrame.loc[row, 'playerID'], dataFrame.loc[row, 'date'])
                        data = pd.read_sql_query(query, cnx)
                        ## append calculated feature value to new feature series
                        newFeature = newFeature.append(data.loc[0], ignore_index=True)
                
        ## remove me after testing!!
        #cursor.execute("alter table inputvectors drop column {0}}".format(featureName))
        ## /remove

        features_end = time.time() - features_start
        
        print ("calculation of features complete....time elapsed : {0}".format(features_end))

        
        query = """
                alter table inputvectors
                add column {0} decimal(7,4)
                """.format(featureName)
        cursor.execute(query)       
        
        
        query = ''
        updates_start = time.time()


        for i in range(len(newFeature.array)):
                if not pd.isna(newFeature[i]):
                        query = """
                                update inputvectors
                                set {0} = {1}
                                where `index` = {2};
                                """.format(featureName, newFeature[i], i+1)
                        cursor.execute(query)
        
        cnx.commit()
                        

        updates_end = time.time() - updates_start
        print ("updates complete....time elapsed : {0}".format(updates_end))

        query = """
                insert into featuresList (name, feature)
                values ("{0}","{1}")
                """.format(featureName,featureQuery)
        cursor.execute(query)
        cnx.commit()

        end_time = time.time() - start_time

        print ("finished adding new feature....total time elapsed : {0}".format(end_time))        