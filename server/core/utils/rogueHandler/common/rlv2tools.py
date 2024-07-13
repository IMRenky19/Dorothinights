from .map import generateSightByVision
from ....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import shuffle, randint, sample, random
from copy import deepcopy
from server.core.utils.json import read_json
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH


ts = time()
rogueTable: dict = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)

         
def getRogueData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.rlv2)

def getRogueExtensionData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.extension)

def getTheme(rlv2_data: dict):
    return rlv2_data["current"]["game"]["theme"]
          
  
def addHpLimit(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] += add
    rlv2_data["current"]["player"]["property"]["hp"]["max"] += add
    
def setHpLimit(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["hp"]["max"] = sets
    
def setHp(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] = sets
    
def getHp(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["hp"]["current"]
def getHpLimit(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["hp"]["max"]
    
def addHp(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] += add
    return hpChecker(rlv2_data)
    
def setExp(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["exp"] = sets
    
def getExp(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["exp"]
    
def addExp(rlv2_data: dict, add: int)-> dict:
    rlv2_data["current"]["player"]["property"]["exp"] += add
    return expChecker(rlv2_data)
    
def setExpLevel(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["level"] = sets
    
def getExpLevel(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["level"]
    
def addExpLevel(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["level"] += add
    
    
def setShield(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["shield"] = sets
    
def getShield(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["shield"]
    
def addShield(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["shield"] += add
    
def setGold(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["gold"] = sets
    
def addGold(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["gold"] += add
    
def getGold(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["gold"]
    
def addCharLimit(extension: dict, add: int):
    extension["extra_char_limit"] += add
    
def setPopulation(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["population"]["max"] = sets
    
def addPopulation(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["population"]["max"] += add
    
def getPopulationCost(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["population"]["cost"]

def getPopulationMax(rlv2_data: dict):
    return rlv2_data["current"]["player"]["property"]["population"]["max"]
    
def setCapacity(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["capacity"] = sets
    
def addCapacity(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["capacity"] += add
    capacityChecker(rlv2_data)
    
def getCurrentState(rlv2_data: dict):
    return rlv2_data["current"]["player"]["state"]

def setCurrentState(rlv2_data: dict, sets: str):
    rlv2_data["current"]["player"]["state"] = sets
    
def getCurrentScene(rlv2ExtensionData: dict):
    return rlv2ExtensionData["currentScene"]

def setCurrentScene(rlv2ExtensionData: dict, sets: str):
    rlv2ExtensionData["currentScene"] = sets

def getCurrentEvent(rlv2ExtensionData: dict):
    return rlv2ExtensionData["currentEvent"]

def setCurrentEvent(rlv2ExtensionData: dict, sets: str):
    rlv2ExtensionData["currentEvent"] = sets
    
def getStartTs(rlv2_data: dict):
    return rlv2_data["current"]["game"]["start"]

def getToEnding(rlv2_data: dict):
    return rlv2_data["current"]["player"]["toEnding"]

def getHardLevel(rlv2_data: dict):
    return rlv2_data["current"]["game"]["modeGrade"]

def getChaos(rlv2_data: dict):
    return rlv2_data["current"]["module"]["chaos"]["chaosList"]

def setPending(rlv2_data: dict, pending: list):
    rlv2_data["current"]["player"]["pending"] = pending
    
def addPending(rlv2_data: dict, pending: dict):
    rlv2_data["current"]["player"]["pending"].append(pending)
    
def popPending(rlv2_data: dict):
    rlv2_data["current"]["player"]["pending"].pop(0)
    
def clearAllPending(rlv2_data: dict):
    rlv2_data["current"]["player"]["pending"] = []
    
def finishNode(rlv2_data: dict):
    currentNode = rlv2_data["current"]["map"]["zones"]\
        [str(getCurrentZone(rlv2_data))]["nodes"][str(positionToIndex(getPosition(rlv2_data)))]
    currentNode["fts"] = ts
    
def isZoneEnd(rlv2_data: dict):
    currentNode = rlv2_data["current"]["map"]["zones"]\
        [str(getCurrentZone(rlv2_data))]["nodes"][str(positionToIndex(getPosition(rlv2_data)))]
    return currentNode["zone_end"]
    
def getVision(rlv2_data: dict):
    return rlv2_data["current"]["module"]["vision"]["value"]

def setVision(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["vision"]["value"] = sets
    
def addVision(rlv2_data: dict, add: int):
    rlv2_data["current"]["module"]["vision"]["value"] += add
    visionChecker(rlv2_data)
    generateSightByVision(getCurrentZone(rlv2_data), getPosition(rlv2_data), getVision(rlv2_data), rlv2_data["current"]["map"]["zones"])
    
def visionChecker(rogueData: dict):
    currentVision = getVision(rogueData)
    if currentVision > 6 and True:          #TODO:琥珀伤痕
        setVision(rogueData, 6)
        rogueData["current"]["module"]["vision"]["isMax"] = True
    if currentVision < 6 and (rogueData["current"]["module"]["vision"]["isMax"]):
        rogueData["current"]["module"]["vision"]["isMax"] = False
    if currentVision < 0:
        setVision(rogueData, 0)
        
def hpChecker(rogueData: dict):
    currentHp = getHp(rogueData)
    currentHpLimit = getHpLimit(rogueData)
    if currentHp > currentHpLimit:
        setHp(rogueData, currentHpLimit)
    if currentHp < 0:
        setHp(rogueData, 1)
        
def capacityChecker(rogueData: dict):
    currentCapacity = getHp(rogueData)
    if currentCapacity > 13:          #TODO:琥珀伤痕
        setVision(rogueData, 13)
    if currentCapacity < 0:
        setVision(rogueData, 0)
        
        
def expChecker(rogueData: dict):
    expTable = [0, 10, 24, 36, 40, 55, 65, 70, 75, 80]
    
    
    currentLevel = getExpLevel(rogueData)
    currentExp = getExp(rogueData)
    
    modifiedLevel = 1
    
    for i in expTable[0:currentLevel]:
        currentExp += i
    
    for i in range(9):
        match currentExp:
            case currentExp if currentExp >= expTable[i + 1]:
                currentExp -= expTable[i + 1]
                modifiedLevel += 1
                continue
            
    setExp(rogueData, currentExp)
    setExpLevel(rogueData, modifiedLevel)
    return levelUpgrade(currentLevel, modifiedLevel, rogueData)
    
def levelUpgrade(currentLevel: int, modifiedLevel: int, rogueData: dict) -> dict:
    theme = getTheme(rogueData)
    tmp = 1
    population = 0
    capacity = 0
    hpLimit = 0
    for i in range(modifiedLevel - currentLevel):
        population += rogueTable["details"][theme]["detailConst"]["playerLevelTable"][str(modifiedLevel + tmp)]["populationUp"]
        capacity += rogueTable["details"][theme]["detailConst"]["playerLevelTable"][str(modifiedLevel + tmp)]["squadCapacityUp"]
        hpLimit += rogueTable["details"][theme]["detailConst"]["playerLevelTable"][str(modifiedLevel + tmp)]["maxHpUp"]
        tmp += 1
    addPopulation(rogueData, population)
    addCapacity(rogueData, capacity)
    addHpLimit(rogueData, hpLimit)
    return {
        "population": population,
        "capacity": capacity,
        "hpLimit": hpLimit
    }
        

def getBand(rlv2_data: dict):
    return rlv2_data["current"]['inventory']['relic']['r_0']['id']

def addRecruitPending(rlv2_data: dict, choiceTicket: str):
    pending_index = getNextPendingIndex(rlv2_data)
    rlv2_data["current"]["player"]["pending"].insert(
        0, {
            "index": pending_index,
            "type": "RECRUIT",
            "content": {
                    "recruit": {
                        "ticket": choiceTicket
                    }
            }
        }
    )

def addTotem(rlv2_data: dict, item: str, enchantment: str = None):
    index = getNextTotemIndex(rlv2_data)
    ts = time()
    rlv2_data["current"]["module"]["totem"]["totemPiece"].append(
        {
            "id": item,
            "index": index,
            "used": False,
            "ts": ts,
            "affix": enchantment
        }
    )
    
def isTotemExist(rlv2_data: dict, totemId: str):
    for totem in rlv2_data["current"]["module"]["totem"]["totemPiece"]:
        if totem["id"] == totemId:
            return True
    return False
    
def addRelic(rlv2_data: dict, item: str):
    index = getNextRelicIndex(rlv2_data)
    ts = time()
    rlv2_data["current"]["inventory"]["relic"][index] = {
            "id": item,
            "index": index,
            "count": 1,
            "ts": ts
    }
    return index
    
def isRelicExist(rlv2_data: dict, relicId: str, rogueExtension: dict):
    realRelic = relicId
    tmp = relicId.split("_")
    canUpgradeIndex = rogueExtension["canUpgradeIndex"]
    if tmp[3] == "legacy" and int(tmp[4]) in canUpgradeIndex:
        if len(tmp) > 5:
            realRelic = "_".join(tmp[:5])
    for relic in rlv2_data["current"]["inventory"]["relic"].values():
        tmp2 = relic["id"].split("_")
        if tmp2[3] == "legacy" and int(tmp2[4]) in canUpgradeIndex:
            if len(tmp2) > 5:
                realRelic2 = "_".join(tmp2[:5])
            else:
                realRelic2 = relic["id"]
        else:
            realRelic2 = relic["id"]
        if realRelic2 == realRelic:
            return True
    return False
    
def addTicketBattle(rlv2_data: dict, item: str, fromWhere = "battle"):
    index = getNextTicketIndex(rlv2_data)
    ts = time()
    rlv2_data["current"]["inventory"]["recruit"][index] = {
            "id": item,
            "index": index,
            "count": 1,
            "ts": ts,
            "state": 0,
            "list": [],
            "result": None,
            "from": fromWhere,
            "mustExtra": 0,
            "needAssist": False
    }
    return index
def removeTotem(rlv2_data: dict, index: str):
    rlv2_data["current"]["module"]["totem"]["totemPiece"][int(index[2:]) - 1]["used"] = True


def getNextTicketIndex(rlv2_data: dict):
    d = set()
    for e in rlv2_data["current"]["inventory"]["recruit"]:
        d.add(int(e[2:]))
    i = 0
    while i in d:
        i += 1
    return f"t_{i}"

def getNextRelicIndex(rlv2_data: dict):
    return f"r_{len(rlv2_data["current"]["inventory"]["relic"])}"

def getNextPendingIndex(rlv2_data: dict):
    d = set()
    for e in rlv2_data["current"]["player"]["pending"]:
        d.add(int(e["index"][2:]))
    i = 0
    while i in d:
        i += 1
    return f"e_{i}"

def getNextTotemIndex(rlv2_data: dict):
    d = set()
    for e in rlv2_data["current"]["module"]["totem"]["totemPiece"]:
        d.add(int(e["index"][2:]))
    i = 0
    while i in d:
        i += 1
    return f"t_{i}"

def getNextCharId(rlv2, charId: str = None, isUpgrade: bool = False):
    i = 0
    if charId:
        for k, char in rlv2["current"]["troop"]["chars"].items():
            if char["charId"] == charId and isUpgrade:
                return k
    while str(i) in rlv2["current"]["troop"]["chars"]:
        i += 1
    return str(i)

def getNextZoneId(rlv2):
    i = 1
    while str(i) in rlv2["current"]["map"]["zones"].keys():
        i += 1
    return int(i)

def getPosition(rlv2_data: dict):
    return rlv2_data["current"]['player']['cursor']['position']

def getCurrentZone(rlv2_data: dict):
    return rlv2_data["current"]['player']['cursor']['zone']

def getModeGrade(rlv2_data: dict):
    return rlv2_data["current"]['game']['modeGrade']

def positionToIndex(position: dict):
    return f"{position["x"]}0{position["y"]}" if position["x"] != 0 else f"{position["y"]}"


def addTicket(rlv2_data: dict, ticket_id: str, init: bool, profession: str = 'all'):
    theme = rlv2_data["current"]["game"]["theme"]
    ticket = f"{theme}_recruit_ticket_{profession}"
    rlv2_data["current"]["inventory"]["recruit"][ticket_id] = {
        "index": ticket_id,
        "id": ticket,
        "state": 0,
        "list": [],
        "result": None,
        "ts": ts,
        "from": "initial",
        "mustExtra": 0,
        "needAssist": init
    }
    rlv2_data["current"]["player"]["pending"][0]["content"]["initRecruit"]["tickets"].append(
        ticket_id
    )

def getActivateTicketList(rlv2_data: dict):
    tmp = []
    for ticket, detail in rlv2_data["current"]["inventory"]["recruit"].items():
        if detail["state"] != 2:
            tmp.append(ticket)
    return tmp
    
   
def getChars(rogueData: dict, rogueExtension: dict, recruitTicketId: str, userSyncData: dict):
    theme = getTheme(rogueData)
    NEW_UPGRADE_BONUS_SYSTEM = True if theme == "rogue_4" else False
    NEW_RECRUIT_POPULATION_COST_SYSTEM = True if theme == "rogue_4" else False
    MIZUKI_ADD_POPULATION_COST = True if theme == "rogue_2" else False
    
    chars = [
        userSyncData["troop"]["chars"][i] 
        for i in userSyncData["troop"]["chars"]
    ]
    match rogueExtension["band_direct_upgrade"]:
        case 0:
            upgradeBonusProfessionList = []
        case 1:
            upgradeBonusProfessionList = ["WARRIOR", "PIONEER"]
        case 2:
            upgradeBonusProfessionList = ["TANK", "SUPPORT"]
        case 3:
            upgradeBonusProfessionList = ["SNIPER", "MEDIC"]
        case 4:
            upgradeBonusProfessionList = ["CASTER", "SPECIAL"]
    isFreeUpgrade: int = rogueExtension["no_upgrade_population"]
    currentChars = rogueData["current"]["troop"]["chars"]
    specialChars = [
        "char_504_rguard",
        "char_514_rdfend",
        "char_505_rcast",
        "char_506_rmedic",
        "char_507_rsnipe"
    ]
    hadChars = {
        char["charId"]: char
        for char in currentChars.values()
    }
    
    canUpgradeChars = {
        char["charId"]: char
        for char in hadChars.values() 
        if char["upgradeLimited"]
    }
    
    isOnlyUpgrade = False if recruitTicketId.find("upgrade") == -1 else True
    ticketDetail = rogueTable["details"][theme]["upgradeTickets"][recruitTicketId]\
                            if isOnlyUpgrade \
                        else rogueTable["details"][theme]["recruitTickets"][recruitTicketId]
    ticketProfessionList = [x
        for x in ticketDetail["professionList"]
    ]
    rarityList = [int(x.split("_")[1])
        for x in ticketDetail["rarityList"]
    ]
    extraCloneChar = ticketDetail["extraCharIds"]
    haveUpgradeBonus = False if recruitTicketId.find("discount") == -1 else True
    rarity6Buff = rogueExtension["upgrade_bonus_6"]
    rarity5Buff = rogueExtension["upgrade_bonus_5"]
    rarity4Buff = rogueExtension["upgrade_bonus_4"]
    isAddPopulationCost = rogueExtension["more_population_cost"]
    
    selectedCharsList = []
    upgradeCharsList = []
    
    for char in chars:
        charProfession = char["profession"]
        charId = char["charId"]
        charRarity = int(char["rarity"])
        if charId in canUpgradeChars.keys() and (charRarity in rarityList) and (charProfession in ticketProfessionList):
            upgradeCharsList.append(char)
            
        if (not (charProfession in ticketProfessionList)) \
            or (not (charRarity in rarityList)) \
            or (charId in hadChars.keys()) \
            or (charId in specialChars):
            continue
        else:
            selectedCharsList.append(char)
    rarity4Dict = {"WARRIOR":[],"PIONEER":[],"TANK":[],"SUPPORT":[],"SNIPER":[],"MEDIC":[],"CASTER":[],"SPECIAL":[]}
    rarity5Dict = {"WARRIOR":[],"PIONEER":[],"TANK":[],"SUPPORT":[],"SNIPER":[],"MEDIC":[],"CASTER":[],"SPECIAL":[]}
    rarity6Dict = {"WARRIOR":[],"PIONEER":[],"TANK":[],"SUPPORT":[],"SNIPER":[],"MEDIC":[],"CASTER":[],"SPECIAL":[]}
    lowRarityDict = {"WARRIOR":[],"PIONEER":[],"TANK":[],"SUPPORT":[],"SNIPER":[],"MEDIC":[],"CASTER":[],"SPECIAL":[]}
    for char in upgradeCharsList:
        charRarity = int(char["rarity"])
        match charRarity:
            case 4:
                rarity = (0 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 1) + (-1 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
            case 5:
                rarity = (1 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 2) + (-1 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
            case 6:
                rarity = (3 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 3) + (-1 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
        char.update(
            {
                "type": "NORMAL",
                "upgradeLimited": False,
                "upgradePhase": 1,
                "isUpgrade": True,
                "isCure": False,
                "population": rarity if not isFreeUpgrade else 0,
                "charBuff": [],
                "troopInstId": canUpgradeChars[char["charId"]]["troopInstId"]
            }
        )
    
    
    for char in selectedCharsList:
        charProfession = char["profession"]
        charId = char["charId"]
        charRarity = int(char["rarity"])
        match charRarity:
            case 4:
                rarity = (0 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 2) + isAddPopulationCost + (-2 if rarity4Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
                rarity4Dict[charProfession].append(char)
            case 5:
                rarity = (2 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 3) + isAddPopulationCost + (-2 if rarity5Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
                rarity5Dict[charProfession].append(char)
            case 6:
                rarity = (6 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 6) + isAddPopulationCost + (-2 if rarity6Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
                rarity6Dict[charProfession].append(char)
            case _:
                rarity = 0 + (isAddPopulationCost if MIZUKI_ADD_POPULATION_COST else 0)
                lowRarityDict[charProfession].append(char)
        char.update(
            {
                "type": "NORMAL",
                "upgradeLimited": False,
                "upgradePhase": 0,
                "isUpgrade": False,
                "isCure": False,
                "population": rarity,
                "charBuff": [],
                "troopInstId": "0"
            }
        )
    
    if NEW_UPGRADE_BONUS_SYSTEM:
        for profession in upgradeBonusProfessionList:
            for char in rarity4Dict[profession]:
                char.update(
                    {
                        "upgradePhase": 1,
                        "upgradeLimited": False
                    }
                )
            for char in rarity5Dict[profession]:
                char.update(
                    {
                        "upgradePhase": 1,
                        "upgradeLimited": False
                    }
                )
            for char in rarity6Dict[profession]:
                char.update(
                    {
                        "upgradePhase": 1,
                        "upgradeLimited": False
                    }
                )
    else:
        for profession in upgradeBonusProfessionList:
            if random() < 0.8:
                waitToUpgrade4 = sample(
                        rarity4Dict[profession], 
                        2 if len(rarity4Dict[profession]) >= 2 else len(rarity4Dict[profession])
                )
                for char in waitToUpgrade4:
                    char.update(
                        {
                            "type": "UPGRADE_BONUS",
                            "upgradePhase": 1,
                            "upgradeLimited": False
                        }
                    )
            if random() < 0.8:
                waitToUpgrade5 = sample(
                    rarity5Dict[profession], 
                    3 if len(rarity5Dict[profession]) >= 3 else len(rarity5Dict[profession])
                )
                for char in waitToUpgrade5:
                    char.update(
                        {
                            "type": "UPGRADE_BONUS",
                            "upgradePhase": 1,
                            "upgradeLimited": False
                        }
                    )
            if random() < 0.35:
                waitToUpgrade6 = sample(
                    rarity6Dict[profession], 
                    6 if len(rarity6Dict[profession]) >= 6 else len(rarity6Dict[profession])
                )
                for char in waitToUpgrade6:
                    char.update(
                        {
                            "type": "UPGRADE_BONUS",
                            "upgradePhase": 1,
                            "upgradeLimited": False
                        }
                    )
    for char in selectedCharsList:
        if char["type"] == "UPGRADE_BONUS" or char["upgradePhase"] == 1:
            continue
        if char["evolvePhase"] <= 1 and len(char["skills"]) < 2:
            char["upgradeLimited"] = False
        if char["evolvePhase"] == 2:
            char["evolvePhase"] = 1
            char["upgradeLimited"] = True
            match int(len(char["skills"])):
                case 0:
                    char["level"] = 55
                case 1:
                    char["level"] = 60
                case 2:
                    char["level"] = 70
                case 3:
                    char["level"] = 80
            if len(char["skills"]) == 3:
                char["defaultSkillIndex"] = 1
                char["skills"][-1]["unlock"] = 0
            for skill in char["skills"]:
                skill["specializeLevel"] = 0
            char["currentEquip"] = None
    for cloneChar in extraCloneChar:
        selectedCharsList.append(
            {
                "charId": cloneChar,
                "type": "THIRD_LOW",
                "evolvePhase": 1,
                "level": 55,
                "exp": 0,
                "favorPoint": 25570,
                "potentialRank": 0,
                "mainSkillLvl": 7,
                "skills": [],
                "defaultSkillIndex": 0,
                "skin": f"{cloneChar}#1",
                "upgradeLimited": False,
                "upgradePhase": 0,
                "isUpgrade": False,
                "isCure": False,
                "population": 0,
                "charBuff": [],
                "troopInstId": "0"
            }
        )
    if isOnlyUpgrade:
        finalCharsList = upgradeCharsList
    else:
        finalCharsList = upgradeCharsList + selectedCharsList
    for char,i in zip(finalCharsList,range(len(finalCharsList))):
        char.update(
            {
                "instId": str(i)
            }
        )
    return finalCharsList