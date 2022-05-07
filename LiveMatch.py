"""
LiveMatch.py

Author: nobiduke
Date: 3.25.2022
Desc: The class that will hold all data for a singular live match from the league of legends api through spectating the match

"""

from LivePlayer import LivePlayer

class LiveMatch:

    def __init__ (self, info, you):
        
        self.gameId = info["gameId"]
        self.mapId = info["mapId"]
        self.gameMode = info["gameMode"]
        self.gameType = info["gameType"]
        self.blue = []
        self.red = []
        self.players = {}

        for player in info["participants"]:
            play = LivePlayer(player)
            
            if play.summonerName == you:
                self.you = play
            
            if play.teamId == 100:
                self.blue.append(play.summonerName)
                self.players[play.summonerName] = play
            else:
                self.red.append(play.summonerName)
                self.players[play.summonerName] = play


    def getNames(self):
        names = []
        for participant in self.players.keys():
            names.append(participant)
        
        return names

    
    def getPlayer(self, name, default=None): return self.players.get(name, default)
