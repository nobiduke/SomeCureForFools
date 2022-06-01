"""
LivePlayer.py

Author: nobiduke
Date: 3.25.2022
Desc: The class that holds the data for a player within a LiveMatch
"""

class LivePlayer:
    def __init__(self, info)->None:
        # identity
        self.summonerName = info["summonerName"]
        self.teamName = "Blue" if info["teamId"] == 100 else "Red"
        self.summonerId = str(info["summonerId"])
        self.teamId = str(info["teamId"])
        
        # the ids :(
        self.perkStyleId = str(info["perks"]["perkStyle"])
        self.perkSubStyleId = str(info["perks"]["perkSubStyle"])
        self.perkIds = info["perks"]["perkIds"]
        self.spell1Id = str(info["spell1Id"])
        self.spell2Id = str(info["spell2Id"])
        self.championId = str(info["championId"])
        self.profileIconId = str(info["profileIconId"])

        # the names :)
        self.championName = str
        self.perkStyle = str
        self.perkSubStyle = str
        self.perkNames = []
        self.spell1 = str
        self.spell2 = str

    def updateInfo(self, data):
        
        # using the DataHold process the ids that the player stores
        self.championName = data.getChampionName(self.championId)
        self.spell1 = data.getSpellName(self.spell1Id)
        self.spell2 = data.getSpellName(self.spell2Id)
        self.perkStyle = data.getPerkStyleName(self.perkStyleId)
        self.perkSubStyle = data.getPerkStyleName(self.perkSubStyleId)

        for idNum in self.perkIds:
            name = data.getRuneName(str(idNum))
            if name:    
                self.perkNames.append(name)


    def fill(self, data):
        # the player info doesn't change throughout so if its already filled, it is immediately stopped
        if self.perkNames:
            return

        self.updateInfo(data)

    
    def getSummonerName(self): return self.summonerName
    def getSummonerId(self): return self.summonerId
    
    
    def getGameInfo(self, data):
        self.fill(data)
        return {"summoner": self.summonerName, "champion": self.championName, "perkStyle": self.perkStyle,
                "perkSubStyle": self.perkSubStyle, "runeList": self.perkNames,
                "spell1": self.spell1, "spell2": self.spell2, "team": self.teamName}
