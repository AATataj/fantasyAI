import mysql.connector
import datetime
import pdb

import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## this file is meant to be an example of utilizing 
## pandas to calculate my day-by-day feature vectors via pandas.dataFrame()
## I will not be listing all the calculated features here as it will be 
## awfully redundant, as well as giving away all my best ideas publicly

def pointsVector(cnx):
        ## necessary data for calculated features
        dataFrame = pd.read_sql_query("select name, playerID from boxscores limit 20", cnx)
        series = pd.read_sql_query("select date from boxscores limit 20", cnx)
        pointsSeries = pd.read_sql_query("select pts from boxscores limit 20", cnx)
        ## build basic dataframe
        dataFrame2 = pd.concat([dataFrame, series, pointsSeries], axis = 1)

        avg7Days = pd.Series()
        #calculate features for each player/date
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
        print (dataFrame2.head())