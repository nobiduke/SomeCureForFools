"""
Player.py
Author: nobiduke
Date: 3.28.2022
Desc: The class that holds player data from a past Match
"""

class Player:
    def __init__(self, info, data) -> None:
        self.summonerId = info["summonerId"]
        self.puuid = info["puuid"]
        self.teamId = str(info["teamId"])

        # useful stats
        self.kills = int(info["kills"])
        self.deaths = int(info["deaths"])
        self.assists = int(info["assists"])
        self.visionScore = int(info["visionScore"])
        self.champLevel = int(info["champLevel"])
        self.totalDamage = int(info["totalDamageDealt"])
        self.totalHealing = int(info["totalHeal"])
        self.turretKills = int(info["turretKills"])
        self.win = info["win"]

        # fun stats
        self.abilityCasts = {"q": info["spell1Casts"], "w": info["spell2Casts"], "e": info["spell3Casts"], "r": info["spell4Casts"],
                             "s1": info["summoner1Casts"], "s2": info["summoner2Casts"]}
        self.ccTime = info["timeCCingOthers"]
        self.consumablesPurchased = info["consumablesPurchased"]
        self.totalTimeSpentDead = info["totalTimeSpentDead"]
        self.pentakills = info["pentaKills"]
        self.goldEarned = info["goldEarned"]
        self.baronKills = info["baronKills"]
        if info.get("challenges"):
            self.challenges = info["challenges"]

        # the ids ):
        self.championId = str(info["championId"])
        self.spell1Id = str(info["summoner1Id"])
        self.spell2Id = str(info["summoner2Id"])
        self.perkStyleId = str(info["perks"]["styles"][0]["style"])
        self.perkSubStyleId = str(info["perks"]["styles"][1]["style"])
        self.perkIds = []

        for style in info["perks"]["styles"]:
            for perk in style["selections"]:
                self.perkIds.append(str(perk["perk"]))

        # the names :)
        self.summonerName = info["summonerName"]
        # using the DataHold process the ids that the player stores
        self.championName = data.getChampionName(self.championId)
        self.championImg = data.getChampionImgFull(self.championId)
        self.spell1 = data.getSpellName(self.spell1Id)
        self.spell2 = data.getSpellName(self.spell2Id)
        self.perkStyle = data.getPerkStyleName(self.perkStyleId)
        self.perkSubStyle = data.getPerkStyleName(self.perkSubStyleId)
        self.perkNames = []

        for idNum in self.perkIds:
            name = data.getRuneName(str(idNum))
            if name:    
                self.perkNames.append(name)


    # gets the general from the start of a game
    def getStartInfo(self):
        return {"summoner": self.summonerName, "champion": self.championName, "perkStyle": self.perkStyle,
                "perkSubStyle": self.perkSubStyle, "runeList": self.perkNames,
                "spell1": self.spell1, "spell2": self.spell2, "team": self.teamName}


    # gets the information related to kills, deaths, and assists
    def getKda(self):
        return {"kills": self.kills, "deaths": self.deaths, "assists": self.assists, "kda": round(float(self.challenges["kda"]), 2),
                "kd": round(self.kills/self.deaths, 2)}


    # returns the death time
    def getTimeDead(self): return self.totalTimeSpentDead


    def returnToMonkey(self):
        return vars(self)
