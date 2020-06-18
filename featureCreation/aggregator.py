import mysql.connector
import sys
import pika
import pandas as pd
import numpy as np
import json
from datetime import datetime

def callback(ch,method,properties,body):
    # extract data from json
    jsonString = body.decode('utf8')
    jsonObj = json.loads(jsonString)
    featureQuery = jsonObj['query']
    featureName = jsonObj['featureName']
    data = pd.read_json(jsonObj['data'])
    
    # create the feature entry in the featuresList table
    query = """
            insert into featuresList2 (feature, name) values ("{0}" , "{1}")
            """.format(featureQuery, featureName)    

    cursor.execute(query)
    cnx.commit()

    # alter the inputvectors table add the new column:
    query = """
            alter table featureVectors
            add column {0} decimal(7,4);
            """.format(featureName)
    cursor.execute(query)
    cnx.commit()

    #inserts to the new column
    for row in data.index:
        if not pd.isna(data.iloc[row].loc[featureName]): 
            query = """
                    update featureVectors
                    set {0} = {1}
                    where playerID = {3} and date = '{2}';
                    """.format(featureName, data.iloc[row].loc[featureName],
                                data.iloc[row].loc['date'], data.iloc[row].loc['playerID'])
            cursor.execute(query)
    print('execute() command completed, on to commit()')
    cnx.commit()
    print('feature added.')


# db conection details

cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel=connection.channel()
channel.basic_consume(queue='aggregator', auto_ack=True, on_message_callback=callback)
print("aggregator ready to consume...")
channel.start_consuming()
connection.close()
