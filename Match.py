"""
Match.py
Author: nobiduke
Date: 3.28.2022
Desc: The class that holds match information from a player's past matches
"""

from Player import Player


class Match:
    def __init__(self, info) -> None:

        self.gameId = str(info["gameId"])
        self.startTimeStamp = str(info["gameStartTimestamp"])
        self.duration = str(info["gameDuration"])
        self.gameMode = info["gameMode"]
        self.mapId = info["mapId"]
        self.teams = {"100": [], "200": []}
        self.participants = {}

        for party in info["participants"]:
            self.participants[party["summonerName"]] = party
            self.teams[str(party["teamId"])].append(party["summonerName"])
    
    # participants
    def getSummoner(self, name, data, default=None): return Player(self.participants.get(name), data) if self.participants.get(name) else default

    # info
    def getInfo(self):
        return {"start": self.startTimeStamp, "duration": self.duration, "mode": self.gameMode, "map": self.mapId}