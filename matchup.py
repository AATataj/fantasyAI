from team import team
import mysql.connector
import pdb
class matchup:
    def __init__ (self, t1, t2, startDate, endDate, cnx):
        self.team1 = t1
        self.team2 = t2
        self.weekStart = startDate
        self.weekEnd = endDate
        self.connex = cnx
        self.cursor = self.connex.cursor()
    def rollDate (self, currDate):
        self.team1.rollDate(currDate)
        self.team2.rollDate(currDate)
    def getWeeklyResult (self):
        for x in range(8):
            if self.team1.weeklyTotals[x] > self.team2.weeklyTotals[x]:
                self.team1.record[0]+1
                self.team2.record[1]+1
            elif self.team2.weeklyTotals[x] > self.team1.weeklyTotals[x]:
                self.team2.record[0]+1
                self.team1.record[1]+1
            else:
                self.team2.record[2]+1
                self.team1.record[2]+1
    def isWeekEnd(self, currDate):
        if self.weekEnd == currDate:
            return True
        return False

            



