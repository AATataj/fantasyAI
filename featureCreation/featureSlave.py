import mysql.connector
import sys
import pika
import pandas as pd
import numpy as np
import json
from datetime import datetime

# this function will take a dataframe which includes :
# name, playerID, date
# and the year of the season, and the query 
# outputs the dataframe of name, playerID, date, 
# and calculated feature values for the given season
# to the cloud storage device.


def callback(ch,method,properties,body):
    # parse the json object here
    jsonString = body.decode('utf8')
    jsonObj = json.loads(jsonString)
    slaveQuery = jsonObj['query']
    startDate = datetime.strptime(jsonObj['args'][0], '%Y-%m-%d')
    endDate = datetime.strptime(jsonObj['args'][1], '%Y-%m-%d')
    featureName = jsonObj['args'][2]
    
    # get a list of all the boxscore rows that need to be solved
    query = """
            select name, playerID, date from boxscores where date >= '{0}' and date <= '{1}'; 
            """.format(startDate, endDate)
    
    print (query)
    data = pd.read_sql_query(query, cnx)
    data[featureName] = np.NaN

    # solve them
    print('solving feature data between {0} and {1}....'.format(startDate, endDate))
    for row in data.index:
        query = slaveQuery.format(data.loc[row]['date'],data.loc[row]['playerID'])
        cursor.execute(query)
        insert = cursor.fetchone()[0]
        data.at[row,featureName] = insert

    
    # send the result to the mq for the aggregator
    print(data.head(10))
    jsonData = data.to_json()
    payload = {}
    payload["featureName"] = featureName
    payload["query"] = slaveQuery
    payload["data"] = jsonData

    payload = json.dumps(payload)
    
    # this code was to check the structure of the json outputted to the payload

    #with open ('payload.json', 'w') as payloadFile:
        #json.dump(payload, payloadFile)

    print('all done for season between {0} and {1}.'.format(startDate, endDate))
    channel.basic_publish(exchange='', 
                          routing_key='aggregator',
                          body=payload
                         )
    

# db conection details

cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()
channel.basic_consume(queue='data', auto_ack=True, on_message_callback=callback)
channel.start_consuming()
connection.close()


