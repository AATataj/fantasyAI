import subprocess
import pika
import mysql.connector
import pandas as pd
from datetime import datetime
import json
import pdb
import time
import os

# read query, feature name, start and end years from json file:
with open('newFeature.json') as json_file:
        data = json.load(json_file)
        featureName = data['featureName']
        startYear = data['startYear']
        endYear = data['endYear']
        slaveQuery = data['query']
        replicas = data['replicas']


# this command is what we're gonna need to launch our slaves
sqlLauncher = """
              docker run -d --name mysql-server -v /var/lib/mysql:/var/lib/mysql mysql
              """
slaveLauncher = """
                docker run -d --name slave{0} feature
                """
slaveLauncher = """
                docker service create --replicas {0} --name slave feature
                """.format(replicas)
swarmStart = "docker swarm init"

# launch the aggregator
aggregatorLauncher = """
                     docker run -d --name aggregator aggregator
                     """

# kill the slaves
teardown2 = """
            docker swarm leave --force
            """
teardown = """
           docker rm $(docker ps -a -q) --force
           """

# create network 
initNetwork = """
              docker network create featureNetwork
              """
connect = """
               docker network connect featureNetwork {0}
               """

# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(queue='data')
channel.queue_declare(queue='aggregator')


# mysql connection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()


# find start and end date of given season 
print ('partitioning the feature creation...')
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


# Create the feature in db
print('creating column in featurevector and adding entry into feature table...')
query = """
        insert into featuresList2 (feature, name) values ("{0}" , "{1}")
        """.format(slaveQuery, featureName)
cursor.execute(query)
cnx.commit()
query = """
        alter table featureVectors
        add column {0} decimal(7,4);
        """.format(featureName)
cursor.execute(query)
cnx.commit()
cnx.close()

# stop the sql localhost instance
print('shutting down local mysql service...')
os.system('sudo /home/slick/fantasy/sqlShutdown.sh')

# Create sql instance :
print ("starting the sql-server...")
sqlStart = subprocess.Popen([sqlLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
sqlStart.wait()

swarmStart = subprocess.Popen([swarmStart], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
swarmStart.wait()
#p = subprocess.Popen([initNetwork], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
#p.wait()
#p = subprocess.Popen([connect.format('mysql-server'],shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
#p.wait()

# RELEASE THE SLAVES! 
print('starting slave service...')
p = subprocess.Popen([slaveLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
p.wait()

# for i in range(replicas):
#         print("starting slave {0}".format(i))
#         p = subprocess.Popen([slaveLauncher.format(i)], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
#         p.wait()
        #p = subprocess.Popen([connect.format('slave'+str(i))],shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        #p.wait()

# Create aggregator
print ("starting the aggregator...")
aggregator = subprocess.Popen([aggregatorLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
p.wait()
#p = subprocess.Popen([connect.format('aggregator')], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
#p.wait()

pdb.set_trace()
while 1:
        ## monitor queue size once every 10 seconds
        time.sleep(10)
        status1 = channel.queue_declare(queue='data', passive=True)
        status2 = channel.queue_declare(queue='aggregator', passive=True)
        ## clean up if queues are both empty
        if status1.method.message_count == 0 and status2.method.message_count == 0:
                break

print ('killing swarm...')
subprocess.Popen([teardown2], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
print("killing slaves, aggregator and mysql-server....")
subprocess.Popen([teardown], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
print("restarting sql service on localhost...")
os.system('sudo /home/slick/fantasy/sqlStart.sh')

connection.close()
print("all done, feature added!")