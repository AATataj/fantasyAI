def mockDraft (self):
        for team in self.teams:
            team.roster = []
            for position in team.lineup:
                team.lineup[position] = None
            ##pdb.set_trace()
            for player in self.freeAgents:
                query = """select * from boxscores where playerID = {} limit 1""".format(player)
                self.cursor = self.connex.cursor(dictionary=True)
                self.cursor.execute(query)
                result = self.cursor.fetchone()
                if(result['position'] == 'G'):
                    if(team.lineup['PG'] == None):
                        team.swapLineup(player, 'PG')
                        team.swapRoster(player)
                        ####self.freeAgents.remove(player)
                        continue
                    if(team.lineup['SG'] ==None):
                        team.swapLineup(player, 'SG')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['G1'] ==None):
                        team.swapLineup(player, 'G1')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['G2'] == None):
                        team.swapLineup(player, 'G2')
                        team.swapRoster(player)
                        continue

                if(result['position'] == 'G-F'):
                    if(team.lineup['SG'] == None):
                        team.swapLineup(player, 'SG')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['SF'] ==None):
                        team.swapLineup(player, 'SF')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['G1'] ==None):
                        team.swapLineup(player, 'G1')
                        team.swapRoster(player)
                        continue
                    if (team.lineup['G2'] == None):
                        team.swapLineup(player, 'G2')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['F1'] ==None ):
                        team.swapLineup(player, 'F1')
                        team.swapRoster(player)
                        continue
                    if team.lineup['F2'] == None:
                        team.swapLineup(player, 'F2')
                        team.swapRoster(player)
                        continue
                if(result['position'] == 'F'):
                    if(team.lineup['SF'] == None):
                        team.swapLineup(player, 'SF')
                        team.swapRoster(player)                            
                        continue
                    if(team.lineup['PF'] ==None):
                        team.swapLineup(player, 'PF')
                        team.swapRoster(player)
                        continue
                    if team.lineup['F1'] ==None:
                        team.swapLineup(player, 'F1')
                        team.swapRoster(player)
                        continue
                    if team.lineup['F2'] ==None:
                        team.swapLineup(player, 'F2')
                        team.swapRoster(player)
                        continue

                if (result['position'] == 'F-C'):
                    if(team.lineup['PF'] == None):
                        team.swapLineup(player, 'PF')
                        team.swapRoster(player)
                        continue
                    if(team.lineup['C1'] ==None):
                        team.swapLineup(player, 'C1')
                        team.swapRoster(player)
                        continue
                    if team.lineup['C2'] ==None:
                        team.swapLineup(player, 'C2')
                        team.swapRoster(player)
                        continue
                    if team.lineup['F1'] ==None:
                        team.swapLineup(player, 'F1')
                        team.swapRoster(player)
                        continue
                    if team.lineup['F2'] ==None:
                        team.swapLineup(player, 'F2')
                        team.swapRoster(player)
                        continue
    
                if (result['position'] == 'C'):
                    if team.lineup['C1'] ==None:
                        team.swapLineup(player, 'C1')
                        team.swapRoster(player)   
                        continue

                    if team.lineup['C2'] ==None:
                        team.swapLineup(player, 'C1')
                        team.swapRoster(player)
                        continue

                if (team.lineup['Util'] ==None):
                    team.swapLineup(player, 'Util')
                    team.swapRoster(player)
                    continue
                if (len(team.roster)<self.teamSize):
                    team.swapRoster(player)
                    continue
                else :
                    pdb.set_trace() 
                    print(team.lineup)
                    break
            for player in team.roster:
                self.freeAgents.remove(player)                
                

        
    