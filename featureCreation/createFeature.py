import subprocess
import pika
import mysql.connector
import pandas as pd
from datetime import datetime
from datetime import timedelta
import json
import pdb
import time
import os, sys

startTime = datetime.now()
# o/s commands we'll need to run the pipeline
sqlLauncher =                   """
                                docker run -d --name mysql-server -v /var/lib/mysql:/var/lib/mysql mysql
                                """
slaveLauncher =                 """
                                docker service create --replicas {0} --name slave feature
                                """
swarmStart =                    """
                                docker swarm init
                                """
aggregatorLauncher =            """
                                docker service create --replicas {0} --name aggr aggregator
                                """
teardown =                      """
                                docker rm mysql-server --force
                                """
teardown2 =                     """
                                docker swarm leave --force
                                """
## docker rm $(docker ps -a -q) --force
def createDBfeature(slaveQuery, featureName):
        # Create the feature in db
        print('creating column in featurevector and adding entry into feature table for {0}...'.format(featureName))
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
        return

def swarmsetup(swarmStart, slaveLauncher, aggregatorLauncher, slaveReplicas, aggregatorReplicas):
        slaveLauncher = slaveLauncher.format(slaveReplicas)
        aggregatorLauncher = aggregatorLauncher.format(aggregatorReplicas)
        # create the docker swarm
        swarmInit = subprocess.Popen([swarmStart], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        swarmInit.wait()
        # RELEASE THE SLAVES! 
        print('starting slave service...')
        p = subprocess.Popen([slaveLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        p.wait()
        # Create aggregator
        print ("starting the aggregator service...")
        aggregator = subprocess.Popen([aggregatorLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        p.wait()
        return

def cleanupSwarm(teardown2):
        print ('killing swarm...')
        subprocess.Popen([teardown2], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        return
def cleanupSQL(teardown):
        print("killing mysql-server....")
        subprocess.Popen([teardown], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        print("restarting sql service on localhost...")
        os.system('sudo /home/slick/fantasy/sqlStart.sh')
        return
def shutdownLocalSQL():
        # stop the sql localhost instance
        print('shutting down local mysql service...')
        cnx.close()
        os.system('sudo /home/slick/fantasy/sqlShutdown.sh')
        return

def createSQLContainer(sqlLauncher):
        # Create sql instance :
        print ("starting the sql-server...")
        sqlStart = subprocess.Popen([sqlLauncher], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        sqlStart.wait()
        return


# mq connection details
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

channel.queue_declare(queue='data')
channel.queue_declare(queue='aggregator')

# mysql connection details
cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

# read query, feature name, start and end years from json file:
with open('newFeature.json') as json_file:
        data = json.load(json_file)
        features = data['features']
        slaveReplicas = data['slaveReplicas']
        aggregatorReplicas = data['aggregatorReplicas']
        for feature in features:
                createDBfeature(feature['query'], feature['featureName'])
                featureName = feature['featureName']
                startYear = feature['startYear']
                endYear = feature['endYear']
                slaveQuery = feature['query']
                # find start and end date of given season 
                print ('partitioning the feature creation for {0}...'.format(featureName))
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
                        currentDate = seasonStart   
                        if 'Season' in featureName:
                                slaveQueryOrig = slaveQuery
                        while currentDate <= seasonEnd:
                                if 'Season' in featureName:
                                        slaveQuery=slaveQuery.format('{0}', '{1}', seasonStart)                                                                        
                                jsonData = '{{"query" : "{0}","args" : ["{1}","{2}", "{3}"]}}'.format(slaveQuery, currentDate, currentDate + timedelta(days=7), featureName)
                                currentDate = currentDate + timedelta(days=8)
                                channel.basic_publish(exchange='', 
                                routing_key='data',
                                body=jsonData
                                )
                        if 'Season' in featureName:
                                slaveQuery = slaveQueryOrig

shutdownLocalSQL()
createSQLContainer(sqlLauncher)
swarmsetup(swarmStart, slaveLauncher, aggregatorLauncher, slaveReplicas, aggregatorReplicas)
while 1:
        ## monitor queue size once every 5 seconds
        time.sleep(5)
        status1 = channel.queue_declare(queue='data', passive=True)
        status2 = channel.queue_declare(queue='aggregator', passive=True)
        ## clean up if queues are both empty
        if status1.method.message_count == 0 and status2.method.message_count == 0:
                break
cleanupSQL(teardown)
cleanupSwarm(teardown2)
connection.close()
print("all done! total runtime : {0}".format(datetime.now() - startTime))
sys.exit()


        



