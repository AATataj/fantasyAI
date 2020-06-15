import subprocess
import pika
import mysql.connector
import sys
import pandas as pd
from datetime import datetime

# get command line args 
startYear = sys.argv[1]
endYear = sys.argv[2]
featureName = sys.argv[3]
# this command is what we're gonna need to launch our slaves
command = """
            kubectl create -f features-deployment.yaml
          """
# but for now, we're testing with one without k8s
command = """
            python3 featureSlave.py
          """

# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='data')

# mysql connection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

# find start and end date of given season 
query = """
        select max(date) from boxscores where date < '{0}-09-01';
        """.format(endYear)
cursor.execute(query)
seasonEnd = cursor.fetchall()
seasonEnd = seasonEnd[0][0]
query = """
        select min(date) from boxscores where date > '{0}-10-01';
        """.format(startYear)
cursor.execute(query)
seasonStart = cursor.fetchall()
seasonStart = seasonStart[0][0]



### this query needs set before each run, it controls slave actions
slaveQuery = """select avg(orb) from boxscores where date < '{0}' and date > date_sub('{0}', interval 7 day) and playerID = {1};"""

jsonData = '{{"query" : "{0}","args" : ["{1}","{2}", "{3}"]}}'.format(slaveQuery, seasonStart, seasonEnd, featureName)
print(jsonData)


## create a loop of messages here
channel.basic_publish(exchange='', 
                      routing_key='data',
                      body=jsonData
                      )


connection.close()

subprocess.run(command, shell=True)


