import mysql.connector
import datetime

def careerAverages(player, date, cursor):
    query = """
            select sum(pts)/count(*) as ppg, sum(trb)/count(*) as rpg, sum(3fgm)/count(*) as 3pg, sum(ast)/count(*) as apg
                   sum(stl)/count(*) as spg, sum(blk)/count(*) as bpg, sum(tov)/count(*) as topg, 
                   sum(fgm)/sum(fga) as fgPer, sum(ftm)/sum(fta) as ftPer
            from boxscores
            where playerID = {0} and date < {1}
            """.format(player, date)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def monthAverages(player, date, cursor):
    query = """
            select sum(pts)/count(*) as ppg, sum(trb)/count(*) as rpg, sum(3fgm)/count(*) as 3pg, sum(ast)/count(*) as apg
                   sum(stl)/count(*) as spg, sum(blk)/count(*) as bpg, sum(tov)/count(*) as topg, 
                   sum(fgm)/sum(fga) as fgPer, sum(ftm)/sum(fta) as ftPer
            from boxscores
            where playerID = {0} and date < {1} and date > {2}
            """.format(player, date, date - timedelta(months=1))
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def weekAverages(player, date, cursor):
    query = """
            select sum(pts)/count(*) as ppg, sum(trb)/count(*) as rpg, sum(3fgm)/count(*) as 3pg, sum(ast)/count(*) as apg
                   sum(stl)/count(*) as spg, sum(blk)/count(*) as bpg, sum(tov)/count(*) as topg, 
                   sum(fgm)/sum(fga) as fgPer, sum(ftm)/sum(fta) as ftPer
            from boxscores
            where playerID = {0} and date < {1} and date > {2}
            """.format(player, date, date - timedelta(weeks=1))
    cursor.execute(query)
    result = cursor.fetchone()
    return result

###########################################
#single category queries
###########################################
def careerPtsAvg(player, date, cursor):
    query = """
            select sum(pts) / count(pts) from boxscores where playerID = {0} and date < {1} and minutes > 0
            """.format(player, date)
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def monthPtsAvg (player, date, cursor):
    query = """
            select sum(pts) / count(pts) from boxscores where playerID = {0} and date < {1} and date > {2} 
            and minutes > 0
            """.format(player, date, date - timedelta(months=1))
    cursor.execute(query)
    result = cursor.fetchone()
    return result

def weekPtsAvg (player, date, cursor):
    query = """
            select sum(pts) / count(pts) from boxscores where playerID = {0} and date < {1} and date > {2} 
            and minutes > 0
            """.format(player, date, date - timedelta(weeks=1))
    cursor.execute(query)
    result = cursor.fetchone()
    return result
