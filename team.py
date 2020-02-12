import mysql.connector
import pdb
class team:
    def __init__(self, ts, ownr, ilsz, cnx):
        self.weeklyTotals = {'fgPer' : 0.0, 'ftPer' : 0.0, '3fgm' : 0, 'pts' : 0, 'ast' : 0, 'trb' : 0,
                    'stl' : 0, 'blk' : 0, 'tov' : 0, 'fgm' : 0, 'fga' : 0, 'ftm' : 0, 'fta' : 0}
        self.lineup = {'PG' : None, 'SG' : None, 'SF' : None, 'PF' : None, 'C1' : None,
                'G1' : None, 'G2' : None, 'F1' : None, 'F2' : None, 'C2' : None, 'Util' : None
            }
        self.record = [0,0,0]
        self.owner = ownr
        self.ilSize = ilsz
        self.teamsize = ts
        self.connex = cnx
        self.cursor = self.connex.cursor(dictionary=True)
        self.record = (0,0,0,0.0)

    def dropPlayer(self, player):
        """drop a player off the roster"""
        for item in self.lineup.items:
            if self.lineup[pos] == player:
                self.lineup[pos] = None
        for index in range (len(self.roster)):
                if playerDrop == index:
                    del roster[index]
        return "Error : Player not found"
        
    def swapRoster(self, playerAdd, playerDrop = None):
        """given a playerID tov add, and potentially one tov remove, swap those roster players"""
        if playerDrop != None:
            self.dropPlayer(playerDrop)
        if len(self.roster) == self.teamsize:
            return "Error: cannot add player.  Over team maxsize"
        else :
            self.roster.append(playerAdd)
            return "Success"

    def swapLineup(self, playerIn, position):
        """given playerID and position of the player, swaps with a position in the lineup"""
        for pos in self.lineup:
            if pos == 'PG' and position == 'PG':
                self.lineup[pos] = playerIn
                return
            if pos == 'C1' and  position == 'C1':
                self.lineup[pos]= playerIn
                return
            if pos == 'C2' and position == 'C2':
                self.lineup[pos]= playerIn
                return
            if pos == 'SG' and position == 'SG':
                self.lineup[pos] = playerIn
                return
            if pos == 'SF' and position == 'SF':
                self.lineup[pos] = playerIn
                return
            if pos == 'PF' and position == 'PF':
                self.lineup[pos] = playerIn
                return
            if pos == 'G1' and position=='G1':
                self.lineup[pos] = playerIn
                return
            if pos == 'G2' and position == 'G2':
                self.lineup[pos] = playerIn
                return
            if pos == 'F1' and position == 'F1':
                self.lineup[pos] = playerIn
                return
            if pos == 'F2' and position == 'F2':
                self.lineup[pos] = playerIn
                return
            if pos == 'Util':
                self.lineup[pos] = playerIn
                return

    def assertLegalRoster (self):
        for item in self.lineup.items:
            if self.lineup[pos] == None:
                return 0
        return 1
    def rollDate(self, currDate):
        for player in self.lineup.values():
            query = "select * from boxscores where playerID = {0} and date = '{1}'".format(player, currDate)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            if result is not None:
                for statistic in self.weeklyTotals:
                    if statistic != 'fgPer' and statistic != 'ftPer':
                        self.weeklyTotals[statistic] += result[statistic]
                self.weeklyTotals['fgPer'] = self.weeklyTotals['fgm']/self.weeklyTotals['fga']
                self.weeklyTotals['ftPer'] = self.weeklyTotals['ftm']/self.weeklyTotals['fta']
        
        return "success"
