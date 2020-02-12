from matchup import matchup
from team import team
import datetime
import mysql.connector
import pdb

class league:
    name = None
    teamSize = 0
    moveLimit = 0
    ILsize = 0
    standings = []
    teams = []
    freeAgents = []
    currentDate = None
    seasonStart = None
    seasonEnd = None
    schedule = None
    connex = None
    cursor = None

    def __init__(self, ts, ml, ilsz, startYear, nm, cnx):
        self.teamSize = ts
        self.moveLimit = ml
        self.name = nm
        self.ILsize = ilsz
        self.connex = cnx
        self.cursor = self.connex.cursor()
        
        query = "select min(date) from boxscores where year(date) = {0} and month(date) > 9".format(startYear)
        self.cursor.execute(query)
        self.seasonStart = self.cursor.fetchone()
        self.seasonStart = self.seasonStart[0]
        self.currentDate = self.seasonStart
        query = "select max(date) from boxscores where year(date) = {0} and month(date) < 9".format(startYear+1)
        self.cursor.execute(query)
        self.seasonEnd = self.cursor.fetchone()
        self.seasonEnd=self.seasonEnd[0]
        query = """select distinct playerHashes.playerID, playerHashes.name 
                from playerHashes
                inner join boxscores
                on playerHashes.playerID = boxscores.playerID
                and (boxscores.date between '{0}' and '{1}')""".format(self.seasonStart.strftime('%Y-%m-%d'), self.seasonEnd.strftime('%Y-%m-%d'))
        self.cursor.execute(query)
        for result in self.cursor:
            self.freeAgents.append(result[0])

    def addTeam(self, team):
        self.teams.append(team)

    def roundRobin(self, sets=None):
        """ Generates a schedule of "fair" pairings from a list of self.teams """
        if len(self.teams) % 2:
            self.teams.append(None)
        count    = len(self.teams)
        sets     = sets or (count - 1)
        half     = count // 2
        schedule = []
        start = self.seasonStart
        end = self.seasonStart + datetime.timedelta(days=6)
        for turn in range(sets):
            pairings = []
            for i in range(half):
                match = matchup(self.teams[i], 
                                self.teams[count-i-1], 
                                start, 
                                end, 
                                self.connex)
                pairings.append(match)
            self.teams.insert(1, self.teams.pop())
            schedule.append(pairings)
            start = self.seasonStart + datetime.timedelta(days=7*(turn+1))
            end = start + datetime.timedelta(days=6)
        return schedule
    def mockDraft(self, team):
        self.cursor = self.connex.cursor(dictionary=True)
        team.roster=[]        
        print(str(len(self.freeAgents)))
        for player in self.freeAgents:
            if len(team.roster) == self.teamSize:
                return
            query = """select * from boxscores where playerID = {0} limit 1""".format(player)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result['position'] == 'PG' or result['position'] == 'G':
                if team.lineup["PG"] == None:
                    team.swapLineup(player, 'PG')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["G1"] == None:
                    team.swapLineup(player, 'G1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["G2"] == None:
                    team.swapLineup(player, 'G2')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                else:
                    continue
                
            if result['position'] == 'SG' or result['position'] == 'G' or result['position'] == 'G-F':
                if team.lineup["SG"] == None:
                    team.swapLineup(player, 'SG')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["G1"] == None:
                    team.swapLineup(player, 'G1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["G2"] == None:
                    team.swapLineup(player, 'G2')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                else:
                    continue

            if result['position'] == 'SF' or result['position'] == 'G-F' or result['position'] == 'F':
                if team.lineup["SF"] == None:
                    team.swapLineup(player, 'SF')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["F1"] == None:
                    team.swapLineup(player, 'F1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["F2"] == None:
                    team.swapLineup(player, 'F2')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                else:
                    continue

            if result['position'] == 'PF' or result['position'] == 'F' or result['position'] == 'F-C':
                if team.lineup["PF"] == None:
                    team.swapLineup(player, 'PF')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue 
                elif team.lineup["C1"] == None:
                    team.swapLineup(player, 'C1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["C2"] == None:
                    team.swapLineup(player, 'C2')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["F1"] == None:
                    team.swapLineup(player, 'F1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["F2"] == None:
                    team.swapLineup(player, 'F2')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup['Util'] == None:
                    team.swapLineup(player, 'Util')
                    team.swapRoster(player)
                else:
                    team.swapRoster(player)
                    continue

            if result['position'] == 'C' or result['position'] == 'F-C':
                if team.lineup["C1"] == None:
                    team.swapLineup(player, 'C1')
                    team.swapRoster(player)
                    #self.freeAgents.remove(player)
                    continue
                elif team.lineup["C2"] == None:
                    team.swapLineup(player, 'C2')
                    team.swapRoster(player)
                    continue     
                else:
                    continue 
    def rollDay (self):
        todoList = []
        for week in self.schedule:
            for match in week:
                if  match.weekStart <= self.currentDate <= match.weekEnd :
                    todoList.append(match)
        print(self.currentDate)
        for match in todoList :
            match.rollDate(self.currentDate)
        
        if self.currentDate == match.weekEnd:
            for statistic in ('pts', 'ast', 'trb', 'stl', 'blk', '3fgm', 'tov', 'ftPer', 'fgPer'):
                if statistic == 'tov':
                    if match.team1.weeklyTotals['tov'] < match.team2.weeklyTotals['tov']:
                        match.team1.record = (1 + match.team1.record[0], match.team1.record[1], \
                                                match.team1.record[2], match.team1.record[3])
                        match.team2.record = (match.team2.record[0],1 + match.team2.record[1], \
                                                match.team2.record[2], match.team2.record[3])
                    elif match.team1.weeklyTotals['tov'] > match.team2.weeklyTotals['tov']:
                        match.team1.record = (match.team1.record[0], 1 + match.team1.record[1], \
                                                match.team1.record[2], match.team1.record[3])
                        match.team2.record = (1 + match.team2.record[0], match.team2.record[1], \
                                                match.team2.record[2], match.team2.record[3])
                    else:
                        match.team1.record = (match.team1.record[0], match.team1.record[1], \
                                                1 + match.team1.record[2], match.team1.record[3])
                        match.team2.record = (match.team2.record[0], match.team2.record[1], \
                                                1 + match.team2.record[2], match.team2.record[3])
                else :
                    if match.team1.weeklyTotals[statistic] > match.team2.weeklyTotals[statistic]:
                        match.team1.record = (1 + match.team1.record[0], match.team1.record[1], \
                                                match.team1.record[2], match.team1.record[3])
                        match.team2.record = (match.team2.record[0], 1 + match.team2.record[1], \
                                                match.team2.record[2], match.team2.record[3])
                    elif match.team1.weeklyTotals[statistic] < match.team2.weeklyTotals[statistic]:
                        match.team1.record = (match.team1.record[0], 1 + match.team1.record[1], \
                                                match.team1.record[2], match.team1.record[3])
                        match.team2.record = (1 + match.team2.record[0], match.team2.record[1], \
                                                match.team2.record[2], match.team2.record[3])
                    else:
                        match.team1.record = (match.team1.record[0], match.team1.record[1], \
                                                1 + match.team1.record[2], match.team1.record[3])
                        match.team2.record = (match.team2.record[0], match.team2.record[1], \
                                                1 + match.team2.record[2], match.team2.record[3])
            match.team1.record = (match.team1.record[0],
                                    match.team1.record[1],
                                    match.team1.record[2],
                                    (match.team1.record[0] + 0.5*match.team1.record[2]) / \
                                    (match.team1.record[0] + match.team1.record[1] + match.team1.record[2]))
            match.team2.record = (match.team2.record[0],
                                    match.team2.record[1],
                                    match.team2.record[2],
                                    (match.team2.record[0] + 0.5*match.team2.record[2]) / \
                                    (match.team2.record[0] + match.team2.record[1] + match.team2.record[2])) 
        self.currentDate = self.currentDate + datetime.timedelta(days=1)
            
                
        