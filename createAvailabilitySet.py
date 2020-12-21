# create availability dataset
# create an availability table containing:
# player name, id, current team, date and :
# latest article and article title given the latest game date of current team
import sys
import mysql.connector
import datetime
import pandas as pd
import pdb

# strategy :
# 1.  take every unique player based on first appearance in boxscores, add those players to the table
# 2.  back fill and forward fill every player that appears in the table for those team's games.
# 3.  find all instances from rotoworld table where player's last entry's team != current entry team
# 4.  remove all entries from table where the team changes mid-season and forward fill games for the new team

def createAvailTable(startYear, cnx):
    cursor = cnx.cursor()
    octMin = datetime.date(startYear, 10, 1)

    query = """
            select * from rotoworld as r2
            inner join 
                (select name, nbaID, playerID, min(date) as date 
                from rotoworld 
                group by name, nbaID, playerID) as r1
            on r2.playerID = r1.playerID and r2.date = r1.date
            """
    cursor.execute(query)
    results = cursor.fetchall()
    
    for result in results:
        team = teamMap(result[1])
        query = """
                insert into tempTable 
                (name, team, recentTitle, recentContent, reportDate, playerID, nbaID)
                values ("{0}","{1}","{2}","{3}","{4}",{5},{6} )
                """.format(result[0], 
                           team, 
                           result[2].replace('"', "'"), 
                           result[3].replace('"', "'"), 
                           result[4], 
                           result[5], 
                           result[6])    
        try :
            cursor.execute(query)
        except :
            print(result[0])
            print(team)
            print(result[2])
            print(result[3])
            print(result[4])
            print(result[5])
            print(result[6])
    cnx.commit()
    return "success!"
    
def addGames(cnx):
    # this function creates a new mirrored table availData
    # and it creates an entry for each player for each game
    # based on the first team they played a game for that season.  

    cursor = cnx.cursor()
    ## gather nba games schedule 2019-2020:
    query = """
            select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
            """
    schedule = pd.read_sql_query(query,cnx)
    schedule.rename(columns={'team':'away', 'opponent' : 'home'}, inplace=True)
    del schedule['homeAway']
    print(len(schedule))
    print(schedule.head())  

    query = """
            select distinct(nbaID), name, team from tempTable;
            """
    players = pd.read_sql_query(query, cnx)

    print(len(players))
    print(players.head())

    for i in range(len(schedule.index)):
        #print(schedule.iloc[i].loc['home'] + " " + schedule.iloc[i].loc['away'] + " " + str(schedule.iloc[i].loc['date']))   
        for j in range(len(players.index)):
            if players.iloc[j].loc['team'] == schedule.iloc[i].loc['home'] or \
                players.iloc[j].loc['team'] == schedule.iloc[i].loc['away']:
                query = """
                        insert into availData
                        (nbaID, name, team, gameDate, home, away)
                        values ({0}, "{1}", "{2}", "{3}", "{4}", "{5}")
                        """.format(
                            players.iloc[j].loc['nbaID'],
                            players.iloc[j].loc['name'],
                            players.iloc[j].loc['team'],
                            schedule.iloc[i].loc['date'],
                            schedule.iloc[i].loc['home'],
                            schedule.iloc[i].loc['away']
                        )
                try:
                    cursor.execute(query)
                except:
                    print(players.iloc[j].loc['nbaID'])
                    print(players.iloc[j].loc['name'])
                    print(players.iloc[j].loc['team'])
                    print(schedule.iloc[i].loc['date'])
                    print(schedule.iloc[i].loc['home'])
                    print(schedule.iloc[i].loc['away'])
    cnx.commit()
    return "success!"
def getLatestArticles(cnx):
    cursor=cnx.cursor()
    query = """
            select nbaID, gameDate from availData
            """
    playersAndDates = pd.read_sql_query(query,cnx)
    for i in range (len(playersAndDates.index)):
        query = """
                select date, title, content 
                from rotoworld 
                where nbaID = {0} and date < '{1}'
                order by date desc
                limit 1 
                """.format(playersAndDates.iloc[i].loc['nbaID'], playersAndDates.iloc[i].loc['gameDate'])
        cursor.execute(query)
        result = cursor.fetchone()
        #print (query)
        if result != None:
            title = result[1].replace('"', "'")
            content = result[2].replace('"', "'")
            insertQuery = """
                        update availData set 
                        recentTitle = "{0}", recentContent = "{1}", reportDate = "{2}"
                        where nbaID = {3} and gameDate = '{4}'
                        """.format(title, content, result[0], 
                            playersAndDates.iloc[i].loc['nbaID'],playersAndDates.iloc[i].loc['gameDate'])
            #print(insertQuery)
            try:
                cursor.execute(insertQuery)
            except :
                e = sys.exc_info()[0]
                print(e)
                print(insertQuery)
    cnx.commit()
    return "success!"
def correctForTrades(cnx):
    cursor = cnx.cursor()
    ## gather nba games schedule 2019-2020:
    query = """
            select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
            """
    schedule = pd.read_sql_query(query,cnx)
    #schedule.rename(columns={'team':'away', 'opponent' : 'home'}, inplace=True)
    #del schedule['homeAway']
    print(len(schedule))
    print(schedule.head())

    query = """
            select b1.nbaID, min(b2.date) as d2, b2.team, b1.name
            from boxscores as b1
            inner join boxscores as b2
            on b1.nbaID = b2.nbaID 
            and b1.team != b2.team
            and b1.date > '{0}'
            where  b1.date < b2.date
            group by b1.nbaID, b2.team, b1.name
            """.format('2019-10-01')
    datesTraded = pd.read_sql_query(query,cnx)



    for i in range(len(datesTraded.index)):
        newTeam = datesTraded.iloc[i].loc['team']
        nbaID = datesTraded.iloc[i].loc['nbaID']
        firstDate = datesTraded.iloc[i].loc['d2']
        name = datesTraded.iloc[i].loc['name']
        query = """
                delete from availData 
                where nbaID = {0} 
                and gameDate >= '{1}'
                """.format(nbaID, firstDate)
        #print(query)
        #pdb.set_trace()
        cursor.execute(query)
        cnx.commit()
        postTradeSched = pd.DataFrame(data=schedule.loc[((schedule['team']==newTeam) | \
            (schedule['opponent']==newTeam)) & (schedule['date'] >= firstDate)])
        for j in range(len(postTradeSched.index)):
            away = postTradeSched.iloc[j].loc['team']
            home = postTradeSched.iloc[j].loc['opponent']
            query = """
                    insert into availData
                    (nbaID, name, team, gameDate, home, away)
                    values ({0}, "{1}", "{2}", "{3}", "{4}", "{5}")
                    """.format(nbaID, name, newTeam, 
                        postTradeSched.iloc[j].loc['date'],
                        home,
                        away
                        )
            try:
                cursor.execute(query)
            except:
                print(query)
        cnx.commit()

    return "success!"
def correctAlecBurks (cnx):
    cursor = cnx.cursor()
    ## gather nba games schedule 2019-2020:
    query = """
            select distinct(date), team, opponent, homeAway from boxscores where date > '2019-10-01' and homeAway = '@';
            """
    schedule = pd.read_sql_query(query,cnx)
    query = """
            delete from availData
            where nbaID = 202692 and gameDate < '2020-02-11'
            """
    cursor.execute(query)
    cnx.commit()
    gswGames = pd.DataFrame(data=schedule.loc[((schedule['team']=='GSW') |
            (schedule['opponent']=='GSW')) & (schedule['date'] < datetime.date(2020,2,11))])
    # print(gswGames.head())
    for i in range (len(gswGames)):
        query = """
                insert into availData (nbaID, name, gameDate, team, home, away)
                values (202692, 'Alec Burks', '{0}', 'GSW', '{1}', '{2}')
                """.format(gswGames.iloc[i].loc['date'],
                           gswGames.iloc[i].loc['opponent'],
                           gswGames.iloc[i].loc['team'] 
                )
        # print(i)
        # print(query)
        cursor.execute(query)
    cnx.commit()
    return "success!"
def teamMap(posTeam):

    ## maps teamPos data to boxscore team abbreviations
    out = ""
    if 'DETROIT PISTONS' in posTeam:
        out = 'DET'
    elif 'OKLAHOMA CITY THUNDER' in posTeam:
        out = 'OKC'
    elif 'NEW ORLEANS PELICANS' in posTeam:
        out = 'NOP'
    elif 'SAN ANTONIO SPURS' in posTeam:
        out = 'SAS'
    elif 'NEW YORK KNICKS' in posTeam:
        out = 'NYK'
    elif 'ATLANTA HAWKS' in posTeam:
        out = 'ATL'
    elif 'BROOKLYN NETS' in posTeam:
        out = 'BRK'
    elif 'BOSTON CELTICS' in posTeam:
        out = 'BOS'
    elif 'INDIANA PACERS' in posTeam:
        out = 'IND'
    elif 'SACRAMENTO KINGS' in posTeam:
        out = 'SAC'
    elif 'PORTLAND TRAIL BLAZERS' in posTeam:
        out = 'POR'
    elif 'UTAH JAZZ' in posTeam:
        out = 'UTA'
    elif 'PHOENIX SUNS' in posTeam:
        out = 'PHX'
    elif 'DENVER NUGGETS' in posTeam:
        out = 'DEN'
    elif 'MINNESOTA TIMBERWOLVES' in posTeam:
        out = 'MIN'
    elif 'LOS ANGELES LAKERS' in posTeam:
        out = 'LAL'
    elif 'LOS ANGELES CLIPPERS' in posTeam:
        out = 'LAC'
    elif 'MEMPHIS GRIZZLIES' in posTeam:
        out = 'MEM'
    elif 'MIAMI HEAT' in posTeam:
        out = 'MIA'
    elif 'TORONTO RAPTORS' in posTeam:
        out = 'TOR'
    elif 'HOUSTON ROCKETS' in posTeam:
        out = 'HOU'
    elif 'CLEVELAND CAVALIERS' in posTeam:
        out = 'CLE'
    elif 'PHILADELPHIA 76ERS' in posTeam:
        out = 'PHI'
    elif 'MILWAUKEE BUCKS' in posTeam:
        out = 'MIL'
    elif 'CHARLOTTE HORNETS' in posTeam:
        out = 'CHO'
    elif 'CHICAGO BULLS' in posTeam:
        out = 'CHI'
    elif 'DALLAS MAVERICKS' in posTeam:
        out = 'DAL'
    elif 'GOLDEN STATE WARRIORS' in posTeam:
        out = 'GSW'
    elif 'ORLANDO MAGIC' in posTeam:
        out = 'ORL'
    elif 'WASHINGTON WIZARDS' in posTeam:
        out = 'WAS'
    return out