"""
Summoner.py

Author: nobiduke
Date: 3.19.2022
Desc: The class that holds all information provided by the summoner tab in the league of legends api
"""

import requests
from Rank import RankInfo
from linkcheck import checkLink
from LiveMatch import LiveMatch
from Match import Match

class Summoner:


    def __init__(self, name, headers, region, regionalLink=None):
        # removes spaces so that the name works for the link
        self.exist = False
        summonerName = "".join(name.split())

        req = requests.get("https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}".format(region=region, summonerName=summonerName), headers=headers)
        
        # makes sure the link is valid
        info = checkLink(req)
        if not info:
            return
        
        req.close()

        # fills in information as neccessary
        self.exist = True
        self.summonerName = name
        self.encryptedId = info["id"]
        self.puuid = info["puuid"]
        self.ranks = []
        self.iconId = info["profileIconId"]
        self.revisionDate = info["revisionDate"]
        self.level = info["summonerLevel"]
        self.region = region
        self.regionalLink = regionalLink

        # print(f"Player: {name}, successfully retrieved")

    
    def __repr__(self):
        return (f"Summoner: {self.summonerName} Region: {self.region}")


    def updateRank(self, headers):
        
        # retrieved data from league api on a users rank
        req = requests.get(f"https://{self.region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{self.encryptedId}", headers=headers)

        # makes sure the request is valid
        info = checkLink(req)
        if not info:
            return

        req.close()

        ranks = []

        # loops through the different ranked queues
        for qType in info:
            ranks.append(RankInfo(qType))

        self.ranks = ranks


    def getRankedSolo(self, headers, default):
        self.updateRank(headers)

        if not self.ranks:
            return default
        
        for rank in self.ranks:
            if rank.isSolo():
                return rank
        
        return default

    
    def getCurrentMatch(self, headers, default):
        req = requests.get(f"https://{self.region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{self.encryptedId}", headers=headers)

        info = checkLink(req)
        if not info:
            return default
        
        req.close()

        return LiveMatch(info, self.summonerName)
        

    def getMatchHistory(self, headers, count=20, default=None, queueType=None):
        headers["count"] = str(count)

        if queueType:
            link = f"https://{self.regionalLink}/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={count}&queue={queueType}"
        else:
            link = f"https://{self.regionalLink}/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&count={count}"

        req = requests.get(link, headers=headers)

        info = checkLink(req)
        if not info:
            return default
        
        req.close()

        return info

    
    def getMatchById(self, headers, idnum, default):
        req = requests.get(f"https://{self.regionalLink}/lol/match/v5/matches/{idnum}", headers=headers)

        info = checkLink(req)
        if not info:
            return default
        
        return Match(info["info"])


    def getMatchDictById(self, headers, idnum, default):
        req = requests.get(f"https://{self.regionalLink}/lol/match/v5/matches/{idnum}", headers=headers)

        info = checkLink(req)
        if not info:
            return default
        
        return info


    def isAlive(self): return self.exist
