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

def pointsVector(cnx):
        cursor = cnx.cursor()
        ## necessary data for calculated features
        dataFrame = pd.read_sql_query("select name, playerID from boxscores limit 20", cnx)
        series = pd.read_sql_query("select date from boxscores limit 20", cnx)
        pointsSeries = pd.read_sql_query("select pts from boxscores limit 20", cnx)
        ## build basic dataframe
        dataFrame2 = pd.concat([dataFrame, series, pointsSeries], axis = 1)

        avg7Days = pd.Series()
        ##calculate features for each player/date
        for row in range(len(dataFrame2)):
                query = """
                        select avg(pts)
                        from boxscores
                        where playerID = {0}
                        and date < '{1}'
                        and date >= date_sub('{1}', interval 7 day) 
                        """.format(dataFrame2.loc[row, 'playerID'], dataFrame2.loc[row, 'date'])
                data = pd.read_sql_query(query, cnx)
                ## append calculated feature value to new feature series
                avg7Days = avg7Days.append(data.loc[0], ignore_index=True)

        ## append calculated feature series to basic dataframe
        dataFrame2['ptsAvg7Days'] = avg7Days

        ## cast date column to a datetime object
        dataFrame2['date'] = pd.to_datetime(dataFrame2['date'], format = '%Y-%m-%d')
        
        #cursor.execute("drop table inputvectors")
        colNames = []
        colTypes = []
        for col in dataFrame2.columns:
                colNames.append(col)
                if dataFrame2[col].dtype == 'object':
                        colTypes.append('varchar(150)')
                if dataFrame2[col].dtype == 'int64':
                        colTypes.append('int')
                if dataFrame2[col].dtype == 'datetime64[ns]':
                        colTypes.append('date')
                if dataFrame2[col].dtype == 'float64':
                        colTypes.append('decimal(7,4)')
                
        query = """
                        create table inputvectors (
                        """
        for i in range(len(colNames)):
                query += colNames[i] + " " + colTypes[i] + ',' 
        query = query[:-1]
        query += ')'
        cursor.execute(query)


        engine = create_engine("mysql://slick:muresan44@localhost/nba")
        con = engine.connect()
        dataFrame2.to_sql(name='inputvectors',index=False, con=con, if_exists='append')
        