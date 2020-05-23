import mysql.connector
import datetime

cnx = mysql.connector.connect(user="slick", password = "muresan44", host ='127.0.0.1', database='nba')
cursor = cnx.cursor()

date = datetime.date(2018,1,22)
featureQuery = """
                select AVG(pts)
                from boxscores
                where playerID = {0}
                and date < '{1}'
                and date >= date_sub('{1}', interval 30 day)
               """.format(213, date, datetime.date(date.year,10,1) if date.month>9 else datetime.date(date.year-1,10,1))
print (featureQuery)
cursor.execute(featureQuery)
out = cursor.fetchone()
print (out)