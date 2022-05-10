"""
User.py

Author: nobiduke
Date: 3.19.2022
Desc: The class that stores all information necessary to run commmands, all commands are run through this class
"""

import requests
from DataHold import DataHold
from Summoner import Summoner
from Player import Player

 # a class for the user to maintain the key and headers for searching
class User:
    def __init__(self, key):
        
        self.data = DataHold(empty=True)
        self.key = key

        # establishes the default headers to be used
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Riot-Token": key
        }

        # makes sure that the key is valid
        testRequest = requests.get("https://na1.api.riotgames.com/lol/platform/v3/champion-rotations", headers=self.headers)

        if testRequest.status_code == 403:
            testRequest.close()
            raise ValueError("Key is expired or invalid")
        
        testRequest.close()


    # creates a holder for all league constants to be accessed
    def createDataHold(self, filename=None):
        self.data = DataHold(filename)        
        self.data.fill()


    # returns a Player class of the given name if one exists, else returns default
    def createSummoner(self, name, region="na1", default=None, regionalLink=None):
        if regionalLink:
            summoner = Summoner(name, self.headers, region, regionalLink)
        elif self.data.isAlive():
            summoner = Summoner(name, self.headers, region, self.data.getRegionByPlatform(region))
        else:
            summoner = Summoner(name, self.headers, region)
        if summoner.isAlive():
            return summoner
        
        return default

    # updates the ranks for a given player, done automatically in all get functions so a little pointless
    def updateRank(self, summoner): summoner.updateRank(self.headers)
    # returns RankInfo type, or the default condition given if there is no RankedSolo
    def getRankedSolo(self, summoner, default=None): return summoner.getRankedSolo(self.headers, default)
    # returns LiveMatch if the summoner is in a match, else default
    def getCurrentMatchBySummmoner(self, summoner, default=None): return summoner.getCurrentMatch(self.headers, default)
    # returns Match if the summoner name is in a match, else default
    def getCurrentMatchByName(self, name, region="na1", default=None): return Summoner(name, self.headers, region).getCurrentMatch(self.headers, default)


    # returns Player given a Match and name
    def getPlayerFromMatch(self, match, summoner, default=None):
        if isinstance(summoner, Summoner):
            return match.getSummoner(summoner.summonerName, self.data, default)
        elif isinstance(summoner, str):
            return match.getSummoner(summoner, self.data, default)
        
        return default
    
    
    # returns Match if the summoner has match in their history
    def getMatchByNumber(self, summoner, index, default=None, queueType=None):
        # makes sure count is valid number that the api will receive
        if index > 99: raise ValueError("Index must be below 99")
        
        # looks for the summoners match history, else returns default
        matchIds = summoner.getMatchHistory(self.headers, default=default, count=(index+1), queueType=queueType)
        if not matchIds: return default
        if index > len(matchIds)-1:
            index = len(matchIds)-1

        return summoner.getMatchById(self.headers, matchIds[index], default)


    # this pings the api key 21 times by default so make sure you put a delay on it if you have a free key
    def getPastGames(self, summoner, count=20, default=None, time=False, queueType=None):
        matchIds = summoner.getMatchHistory(self.headers, count, default, queueType)
        matches = []
        duration = 0

        for idnum in matchIds:
            info = summoner.getMatchDictById(self.headers, idnum, default)
            index = info["metadata"]["participants"].index(summoner.puuid)
            matches.append(Player(info["info"]["participants"][index], self.data))
            duration += int(info["info"]["gameDuration"])
        
        if time:
            return matches, duration
        return matches


    # closes the DataHold
    def close(self):
        try:
            self.data.close()
        except TypeError:
            print("No DataHold exists within this User.")
