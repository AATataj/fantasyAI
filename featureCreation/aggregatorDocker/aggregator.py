import mysql.connector
import sys
import pika
import pandas as pd
import numpy as np
import json
from datetime import datetime
import subprocess

def callback(ch,method,properties,body):
    # extract data from json
    jsonString = body.decode('utf8')
    jsonObj = json.loads(jsonString)
    featureQuery = jsonObj['query']
    featureName = jsonObj['featureName']
    data = pd.read_json(jsonObj['data'])
    
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
    cnx.commit()
    print ('weekly block inserted')
    # manually send ack to queue
    ch.basic_ack(delivery_tag = method.delivery_tag)

# db conection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='172.17.0.2', database='nba')
cursor = cnx.cursor()

# mq connection details
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
creds = pika.PlainCredentials('slick','muresan44')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.1', 5672, '/', creds)) # , hearbeat = 0
channel=connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='aggregator', auto_ack=False, on_message_callback=callback)
print("aggregator ready to consume...")
channel.start_consuming()
connection.close()
