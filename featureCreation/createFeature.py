import subprocess
import pika
import mysql.connector
import pandas as pd
from datetime import datetime
import json

# read query, feature name, start and end years from json file:
with open('newFeature.json') as json_file:
        data = json.load(json_file)
        featureName = data['featureName']
        startYear = data['startYear']
        endYear = data['endYear']
        slaveQuery = data['query']


# this command is what we're gonna need to launch our slaves
command = """
            kubectl create -f features-deployment.yaml
          """
# but for now, we're testing with one without k8s
command = """
            python3 featureSlave.py
          """
command2 = """
            python3 aggregator.py
           """
command3 = """
             kubectl delete namespace='featureCreation'
           """

# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
status1 = channel.queue_declare(queue='data')
status2 = channel.queue_declare(queue='aggregator')


# mysql connection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()


# find start and end date of given season 
for year in range(int(startYear), int(endYear) + 1):

        query = """
                select max(date) from boxscores where date < '{0}-09-01';
                """.format(year+1)
        cursor.execute(query)
        seasonEnd = cursor.fetchall()
        seasonEnd = seasonEnd[0][0]
        query = """
                select min(date) from boxscores where date > '{0}-10-01';
                """.format(year)
        cursor.execute(query)
        seasonStart = cursor.fetchall()
        seasonStart = seasonStart[0][0]
        
        # create json data and use it as payload to a message in the mq
        jsonData = '{{"query" : "{0}","args" : ["{1}","{2}", "{3}"]}}'.format(slaveQuery, seasonStart, seasonEnd, featureName)
        channel.basic_publish(exchange='', 
                      routing_key='data',
                      body=jsonData
                      )



connection.close()

# RELEASE THE SLAVES! 
subprocess.Popen([command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
aggregator = subprocess.Popen([command2], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)

if status1.method.message_count == 0 and status2.method.message_count == 0:
        aggregator.kill()
        subprocess.Popen([command3], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        ## command that will kill the slaves
