"""
Rank.py

Author: nobiduke
Date: 3.19.2022
Desc: The class that holds all ranked information for a Player
"""


class RankInfo:
    def __init__(self, info):

        self.leagueId = info["leagueId"]
        self.queueType = info["queueType"]
        self.queueName = " ".join(self.queueType.split('_')).title()
        self.tier = info["tier"]
        self.division = info["rank"]
        self.lp = info["leaguePoints"]
        self.wins = info["wins"]
        self.losses = info["losses"]
        self.hotStreak = info["hotStreak"]
        self.inactive = info["inactive"]
        
        if info.get("miniSeries"):
            self.series = info["miniSeries"]
        else:
            self.series = None

    def __repr__ (self):
        return (f"Type: {self.queueName}, Rank: {self.tier} {self.division}, Wins: {self.wins}, Losses: {self.losses}")

    def isSolo (self):
        return (True if self.queueType == "RANKED_SOLO_5x5" else False)
