"""
DataHold.py

Author: nobiduke
Date: 3.25.2022
Desc: The class that holds all of the constants for league of legends information that is processed through the api
"""

import json
import requests
from linkcheck import checkLink


class DataHold:
    
    def __init__(self, filename=None, empty=False) -> None:
        if empty:
            self.exist = False
            return

        self.exist = True
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8"
        }

        if filename:
            try:
                with open(filename, "r") as inFile:
                    temp = json.load(inFile)
                    
                    self.platforms = temp["platforms"]
                    self.regionalLinks = temp["regionalLinks"]
                    self.version = temp["version"]
                    self.champions = temp["champions"]
                    self.runes = temp["runes"]
                    self.runeGenre = temp["runeGenre"]
                    self.perkStyles = temp["perkStyles"]
                    self.spells = temp["spells"]
                    self.updates = temp["updates"]
                    self.queueTypes = temp["queueTypes"]
                    self.isChanged = temp["isChanged"]
                    inFile.close()
                    
                    return
            except FileNotFoundError:
                print(f"File: {filename}, does not exist, creating new DataHold...")
            except KeyError:
                print(f"Missing required field in DataHold file, creating new DataHold...")
            
        # establish the data dragon version, if no file was given
        r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", headers=self.headers)
        
        self.platforms = json.load(open("platforms.json", "r"))
        self.regionalLinks = json.load(open("regionalLinks.json", "r"))

        self.version = r.json()[0]
        self.updates = {"champions": None, "runes": None, "spells": None, "queueTypes": None}
        self.champions = {}
        self.runes = {}
        self.runeGenre = {}
        self.perkStyles = {}
        self.spells = {}
        self.queueTypes = {}
        self.isChanged = True


    def getUpdate(self)->bool:
        # returns true if the version had an update, else false
        r = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", headers=self.headers)
        
        if r.json()[0] != self.version:
            self.version = r.json()[0]
            self.isChanged = True
            return True
        else:
            return False


    def updateChamps(self)->None:
        # resets champions to deal with double key writing
        self.champions = {}

        # establish champions.json
        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json", headers=self.headers)
        
        champions = checkLink(r)

        if not champions:
            # print("Failed to update champions.")
            return

        r.close()

        THE_CHAMPS = {}

        for championName in champions["data"]:
            champInfo = champions["data"][championName]
            idnum = str(champInfo["key"])

            THE_CHAMPS[idnum] = {}
            THE_CHAMPS[idnum]["id"] = champInfo["id"]
            THE_CHAMPS[idnum]["name"] = champInfo["name"]
            THE_CHAMPS[idnum]["title"] = champInfo["title"]
            THE_CHAMPS[idnum]["blurb"] = champInfo["blurb"]
            THE_CHAMPS[idnum]["image"] = champInfo["image"]["full"]
        
        self.champions = THE_CHAMPS
        self.updates["champions"] = self.version
        self.isChanged = True


    def updateRunes(self)->None:
        # reset runes because it was double writing keys
        self.runes = {}
        self.runeGenre = {}
        self.perkStyles = {}

        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/runesReforged.json", headers=self.headers)
        
        runes = checkLink(r)

        if not runes:
            # print("Failed to update runes.")
            return

        r.close()

        # iterates three times to get through data dragons style and get just the important rune information
        for cat in runes:
            self.runeGenre[cat["key"]] = []
            self.perkStyles[str(cat["id"])] = cat["key"]
            for runeType in cat["slots"]:
                for rune in runeType["runes"]:
                    self.runeGenre[cat["key"]].append(rune["id"])
                    self.runes[str(rune["id"])] = {"key": rune["key"], "name": rune["name"], "img": ("https://ddragon.canisback.com/img/" + rune["icon"])}

        self.updates["runes"] = self.version
        self.isChanged = True


    def updateSpells(self)->None:
        # reset spells because it was double writing keys
        self.spells = {}

        r = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/summoner.json", headers=self.headers)

        spells = checkLink(r)
        if not spells:
            # print("Failed to update spells.")
            return

        r.close()

        # iterates through the data portion of summoner.json to make a dict with "id": "name"
        for cat in spells["data"]:
            self.spells[spells["data"][cat]["key"]] = spells["data"][cat]["name"]

        self.updates["spells"] = self.version
        self.isChanged = True

    
    def updateQueueTypes(self)->None:
        req = requests.get("https://static.developer.riotgames.com/docs/lol/queues.json", headers=self.headers)

        info = checkLink(req)
        if not info:
            return

        req.close()

        for tip in info:
            if not tip["notes"]:
                self.queueTypes[tip["queueId"]] = tip["description"] 

        self.updates["queueTypes"] = self.version
        self.isChanged = True


    def isUpdatedAndFilled(self):
        self.getUpdate()
        
        for value in self.updates.values():
            if value != self.version: return False
        
        return True


    def isFull(self)->bool:
        if not self.updates["champions"] or not self.updates["runes"] or not self.updates["spells"] or not self.updates["queueTypes"]: return False
        return True

    
    # makes sure every hold is filled, doesn't make sure that they are up to date
    def fill(self):
        if not self.updates["champions"]: self.updateChamps()
        if not self.updates["runes"]: self.updateRunes()
        if not self.updates["spells"]: self.updateSpells()
        if not self.updates["queueTypes"]: self.updateQueueTypes()
    

    # makes sure that every hold is up to date, use with self.getUpdate() for the greatest accuracy
    def update(self):
        if self.updates["champions"] != self.version: self.updateChamps()
        if self.updates["runes"] != self.version: self.updateRunes()
        if self.updates["spells"] != self.version: self.updateSpells()
        if self.updates["queueTypes"] != self.version: self.updateQueueTypes()


    # spells
    def getSpellName(self, idNum, default=None): 
        try: return self.spells[idNum]
        except KeyError: return default
    # runes
    def getRuneName(self, idNum, default=None): 
        try: return self.runes[idNum]["name"]
        except KeyError: return default
    def getRuneImg(self, idNum, default=None): 
        try: return self.runes[idNum]["img"]
        except KeyError: return default
    def getPerkStyleName(self, idNum, default=None): 
        try: return self.perkStyles[idNum]
        except KeyError: return default
    # champions
    def getChampionName(self, idNum, default=None): 
        try: return self.champions[idNum]["name"] 
        except KeyError: return default
    def getChampionIconImg(self, idNum, default=None): 
        try: return self.champions[idNum]["image"]
        except KeyError: return default
    def getChampionBlurb(self, idNum, default=None): 
        try: return self.champions[idNum]["blurb"]
        except KeyError: return default
    def getChampionTitle(self, idNum, default=None): 
        try: return self.champions[idNum]["title"]
        except KeyError: return default
    # platforms
    def getRegionalByPlatform(self, platform, default=None):
        try: return self.regionalLinks[self.platforms[platform]]
        except KeyError: return default

    # for checking existence
    def isAlive(self): return self.exist


    def close(self, filename="datahold.json"):
        # updates the file if the file has modified
        if self.isChanged:
            self.isChanged = False
            
            with open(filename, "w") as outFile:
                json.dump(vars(self), outFile, indent='\t')
                outFile.close()
