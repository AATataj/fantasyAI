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


## get ip address of mysql instance
getIP = """ 
        docker inspect mysql-server | grep '"IPAddress"' | head -n 1 
        """

p = subprocess.Popen([getIP], shell=True, stdin=None, stdout=subprocess.PIPE, stderr=None, close_fds=True)
p.wait()
ipAddr, err = p.communicate()
ipAddr = str(ipAddr)
ipAddr = ipAddr.replace('"IPAddress": "', "")
ipAddr = ipAddr.replace("b'", "")
ipAddr = ipAddr.replace('",\\n', "")
ipAddr = ipAddr.replace("'", "")
ipAddr = ipAddr.strip()
print (ipAddr)

# db conection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='172.17.0.2', database='nba')
cursor = cnx.cursor()

# mq connection details
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
creds = pika.PlainCredentials('slick','muresan44')
connection = pika.BlockingConnection(pika.ConnectionParameters('172.17.0.1', 5672, '/', creds, heartbeat=0))
channel=connection.channel()
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='aggregator', auto_ack=True, on_message_callback=callback)
print("aggregator ready to consume...")
channel.start_consuming()
connection.close()
