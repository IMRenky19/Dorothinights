from server.core.utils.rogueHandler.common.map import NodeType
from ....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import sample, random
from copy import deepcopy
from server.core.utils.json import read_json
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH


ts = time()
rogueTable: dict = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)

         
def getRogueData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.rlv2)

def getRogueExtensionData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.extension)

def getTheme(rogueData: dict):
    return rogueData["current"]["game"]["theme"]
def writeExtraResponseData(rogueData: dict, rogueExtension: dict, extraData: dict):
    responseData = rogueExtension["extraResponse"]
    if responseData:
        if responseData.__contains__("items") and extraData.__contains__("items"):
            responseData["items"] += extraData["items"]
        if responseData.__contains__("pushMessage") and extraData.__contains__("pushMessage"):
            responseData["pushMessage"] += extraData["pushMessage"]
    else:
        responseData.update(extraData)
    #rogueExtension["extraResponse"] = {
    #    "items": items,
    #    "pushMessage":[
    #        {
    #            "path":"rlv2GotRandRelic",
    #            "payload":{
    #                "idList":itemsId
    #            }
    #        }
    #    ]
    #}
    rogueExtension["isNewExtraResponse"] = True

def clearExtraResponseData(rogueData: dict, rlv2Extension: dict):
    if rlv2Extension["isNewExtraResponse"]:
        rlv2Extension["isNewExtraResponse"] = False
    else:
        rlv2Extension["extraResponse"] = {}
    if rlv2Extension["newZoneChaos"]:
        rlv2Extension["newZoneChaos"] = False
    else:
        rogueData["current"]["module"]["chaos"]["deltaChaos"] = {
            "deltaChaos": {
                "preLevel": 0,
                "afterLevel": 0,
                "dValue": 0,
                "dChaos":[]
            }
        }
          
  
def addHpLimit(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["hp"]["current"] += add
    rogueData["current"]["player"]["property"]["hp"]["max"] += add
    
def setHpLimit(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["hp"]["max"] = sets
    
def setHp(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["hp"]["current"] = sets
    
def getHp(rogueData: dict):
    return rogueData["current"]["player"]["property"]["hp"]["current"]
def getHpLimit(rogueData: dict):
    return rogueData["current"]["player"]["property"]["hp"]["max"]
    
def addHp(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["hp"]["current"] += add
    return hpChecker(rogueData)
    
def setExp(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["exp"] = sets
    
def getExp(rogueData: dict):
    return rogueData["current"]["player"]["property"]["exp"]
    
def addExp(rogueData: dict, add: int)-> dict:
    rogueData["current"]["player"]["property"]["exp"] += add
    return expChecker(rogueData)
    
def setExpLevel(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["level"] = sets
    
def getExpLevel(rogueData: dict):
    return rogueData["current"]["player"]["property"]["level"]
    
def addExpLevel(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["level"] += add
    
    
def setShield(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["shield"] = sets
    
def getShield(rogueData: dict):
    return rogueData["current"]["player"]["property"]["shield"]
    
def addShield(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["shield"] += add
    
def setGold(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["gold"] = sets
    
def addGold(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["gold"] += add
    
def getGold(rogueData: dict):
    return rogueData["current"]["player"]["property"]["gold"]
    
def addCharLimit(extension: dict, add: int):
    extension["extra_char_limit"] += add
    
def setPopulation(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["population"]["max"] = sets
    
def addPopulation(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["population"]["max"] += add
    
def getPopulationCost(rogueData: dict):
    return rogueData["current"]["player"]["property"]["population"]["cost"]

def getPopulationMax(rogueData: dict):
    return rogueData["current"]["player"]["property"]["population"]["max"]

def getPopulation(rogueData: dict):
    return getPopulationMax(rogueData) - getPopulationCost(rogueData)
    
def setCapacity(rogueData: dict, sets: int):
    rogueData["current"]["player"]["property"]["capacity"] = sets
    
def addCapacity(rogueData: dict, add: int):
    rogueData["current"]["player"]["property"]["capacity"] += add
    capacityChecker(rogueData)
    
def getCurrentState(rogueData: dict):
    return rogueData["current"]["player"]["state"]

def setCurrentState(rogueData: dict, sets: str):
    rogueData["current"]["player"]["state"] = sets
    
def getCurrentScene(rlv2ExtensionData: dict):
    return rlv2ExtensionData["currentScene"]

def setCurrentScene(rlv2ExtensionData: dict, sets: str):
    rlv2ExtensionData["currentScene"] = sets

def getCurrentEvent(rlv2ExtensionData: dict):
    return rlv2ExtensionData["currentEvent"]

def setCurrentEvent(rlv2ExtensionData: dict, sets: str):
    rlv2ExtensionData["currentEvent"] = sets
    
def getStartTs(rogueData: dict):
    return rogueData["current"]["game"]["start"]

def getToEnding(rogueData: dict):
    return rogueData["current"]["player"]["toEnding"]

def getHardLevel(rogueData: dict):
    return rogueData["current"]["game"]["modeGrade"]

def setPending(rogueData: dict, pending: list):
    rogueData["current"]["player"]["pending"] = pending
    
def addPending(rogueData: dict, pending: dict):
    if rogueData["current"]["player"]["pending"] and rogueData["current"]["player"]["pending"][0]["type"] == "BATTLE" and pending["type"] == "BATTLE" and rogueData["current"]["player"]["pending"][0]["content"]["battle"]["state"] == 0 and pending["content"]["battle"]["state"] == 1:
        rogueData["current"]["player"]["pending"][0].update(pending)
    else:
        rogueData["current"]["player"]["pending"].insert(0, pending)
    
def popPending(rogueData: dict):
    rogueData["current"]["player"]["pending"].pop(0)
    
def clearAllPending(rogueData: dict):
    rogueData["current"]["player"]["pending"] = []
    
def finishNode(rogueData: dict):
    currentNode = rogueData["current"]["map"]["zones"]\
        [str(getCurrentZone(rogueData))]["nodes"][str(positionToIndex(getPosition(rogueData)))]
    currentNode["fts"] = ts
    
def isZoneEnd(rogueData: dict):
    currentNode = rogueData["current"]["map"]["zones"]\
        [str(getCurrentZone(rogueData))]["nodes"][str(positionToIndex(getPosition(rogueData)))]
    return currentNode["zone_end"]

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
        setCapacity(rogueData, 13)
    if currentCapacity < 0:
        setCapacity(rogueData, 0)
        
        
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
        

def getBand(rogueData: dict):
    return rogueData["current"]['inventory']['relic']['r_0']['id']

def addRecruitPending(rogueData: dict, choiceTicket: str):
    pending_index = getNextPendingIndex(rogueData)
    rogueData["current"]["player"]["pending"].insert(
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

def addTotem(rogueData: dict, item: str, enchantment: str | None = None):
    index = getNextTotemIndex(rogueData)
    ts = time()
    rogueData["current"]["module"]["totem"]["totemPiece"].append(
        {
            "id": item,
            "index": index,
            "used": False,
            "ts": ts,
            "affix": enchantment
        }
    )
    
def getTotemList(rogueData: dict):
    return rogueData["current"]["module"]["totem"]["totemPiece"]
    
def isTotemExist(rogueData: dict, totemId: str):
    for totem in rogueData["current"]["module"]["totem"]["totemPiece"]:
        if totem["id"] == totemId:
            return True
    return False
    
def addRelic(rogueData: dict, item: str):
    index = getNextRelicIndex(rogueData)
    ts = time()
    rogueData["current"]["inventory"]["relic"][index] = {
            "id": item,
            "index": index,
            "count": 1,
            "ts": ts
    }
    return index

def removeRelic(rogueData: dict, rogueExtension: dict, index: str):
    rogueData["current"]["inventory"]["relic"][index]["count"] = 0
    
def getItemCount(rogueData: dict, rogueExtension: dict, itemId: str) -> list:
    match itemId:
        case itemId if itemId.find("relic") != -1:
            result = isRelicExist(rogueData, itemId, rogueExtension)
            if result:
                return [result[2], result[1]]
            else:
                return [0]
        case itemId if itemId.find("chaos") != -1:
            return [rogueData["current"]["module"]["chaos"]["value"]]
        case itemId if itemId.find("vision") != -1:
            return [rogueData["current"]["module"]["vision"]["value"]]
        case itemId if itemId.find("hpmax") != -1:
            return [getHpLimit(rogueData)]
        case itemId if itemId.find("hp") != -1:
            return [getHp(rogueData)]
        case itemId if itemId.find("population") != -1:
            return [getPopulation(rogueData)]
        case itemId if itemId.find("gold") != -1:
            return [getGold(rogueData)]
        case itemId if itemId.find("shield") != -1:
            return [getShield(rogueData)]
        case itemId if itemId.find("flag") != -1:
            return [
                rogueExtension["eventFlag"].count(itemId)
            ]
        case _:
            return []

def getRelicData(rogueData: dict, rogueExtension: dict, itemId: str):
    return rogueData["current"]["inventory"]["relic"][itemId]

def isRelicExist(rogueData: dict, relicId: str, rogueExtension: dict, neededLevel: int = 0):
    realRelic = relicId
    tmp = relicId.split("_")
    canUpgradeIndex = rogueExtension["canUpgradeIndex"]
    if tmp[3] == "legacy" and int(tmp[4]) in canUpgradeIndex:
        if len(tmp) > 5:
            realRelic = "_".join(tmp[:5])
    for relic in [x for x in rogueData["current"]["inventory"]["relic"].values() if x["count"] != 0]:
        tmp2 = relic["id"].split("_")
        if tmp2[3] == "legacy" and int(tmp2[4]) in canUpgradeIndex:
            level = tmp2[5] if len(tmp2) > 5 else None
            match neededLevel:
                case 0:
                    canLevel = [None, "a", "b", "c"]
                case 1:
                    canLevel = ["a", "b", "c"]
                case 2:
                    canLevel = ["b", "c"]
                case 3:
                    canLevel = ["c"]
                case _:
                    canLevel = ["?"]
            if not(level in canLevel):
                return []
            if len(tmp2) > 5:
                realRelic2 = "_".join(tmp2[:5])
            else:
                realRelic2 = relic["id"]
        else:
            realRelic2 = relic["id"]
        if realRelic2 == realRelic:
            return [True, relic["index"], relic["count"]]
    return []

def addRelicLayer(rogueData:dict, index:str, add: int):
    if rogueData["current"]["inventory"]["relic"][index].__contains__("layer"):
        rogueData["current"]["inventory"]["relic"][index]["layer"] += add
    else:
        rogueData["current"]["inventory"]["relic"][index]["layer"] = 0
        rogueData["current"]["inventory"]["relic"][index]["layer"] += add
        
def setRelicLayer(rogueData:dict, index:str, sets: int):
    rogueData["current"]["inventory"]["relic"][index]["layer"] = sets
    
def getRelicLayer(rogueData: dict, index: str):
    return rogueData["current"]["inventory"]["relic"][index]["layer"] if rogueData["current"]["inventory"]["relic"][index].__contains__("layer") else 0
    
def addTicketBattle(rogueData: dict, item: str, fromWhere = "battle"):
    index = getNextTicketIndex(rogueData)
    ts = time()
    rogueData["current"]["inventory"]["recruit"][index] = {
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


def removeTotem(rogueData: dict, index: str):
    rogueData["current"]["module"]["totem"]["totemPiece"][int(index[2:]) - 1]["used"] = True


def getNextTicketIndex(rogueData: dict):
    d = set()
    for e in rogueData["current"]["inventory"]["recruit"]:
        d.add(int(e[2:]))
    i = 0
    while i in d:
        i += 1
    return f"t_{i}"

def getNextRelicIndex(rogueData: dict):
    return f"r_{len(rogueData['current']['inventory']['relic'])}"

def getNextPendingIndex(rogueData: dict):
   # d = set()
   # for e in rogueData["current"]["player"]["pending"]:
   #     d.add(int(e["index"][2:]))
   # i = 0
   # while i in d:
   #     i += 1
    return f"e_{len(rogueData["current"]["player"]["pending"])}"

def getNextTotemIndex(rogueData: dict):
    d = set()
    for e in rogueData["current"]["module"]["totem"]["totemPiece"]:
        d.add(int(e["index"][2:]))
    i = 0
    while i in d:
        i += 1
    return f"t_{i}"

def getNextCharId(rlv2, charId: str | None = None, isUpgrade: bool = False):
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

def getPosition(rogueData: dict):
    return rogueData["current"]['player']['cursor']['position']

def getNodeType(rogueData: dict) -> NodeType:
    if getPosition(rogueData):
        return rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]["type"]
    else:
        return NodeType.NONE

def getCurrentZone(rogueData: dict) -> int:
    return rogueData["current"]['player']['cursor']['zone']

def getModeGrade(rogueData: dict):
    return rogueData["current"]['game']['modeGrade']

def positionToIndex(position: dict):
    return f"{position['x']}0{position['y']}" if position["x"] > 0 else f"{position['y']}"


def addTicket(rogueData: dict, ticket_id: str, init: bool, profession: str = 'all'):
    theme = rogueData["current"]["game"]["theme"]
    ticket = f"{theme}_recruit_ticket_{profession}"
    rogueData["current"]["inventory"]["recruit"][ticket_id] = {
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
    rogueData["current"]["player"]["pending"][0]["content"]["initRecruit"]["tickets"].append(
        ticket_id
    )

def getActivateTicketList(rogueData: dict):
    tmp = []
    for ticket, detail in rogueData["current"]["inventory"]["recruit"].items():
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
        case _:
            upgradeBonusProfessionList = []
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
    if isOnlyUpgrade:
        isFreeUpgrade = True
    ticketDetail = rogueTable["details"][theme]["upgradeTickets"][recruitTicketId]\
                            if isOnlyUpgrade \
                        else rogueTable["details"][theme]["recruitTickets"][recruitTicketId]
    ticketProfessionList = [x
        for x in ticketDetail["professionList"]
    ]
    rarityList = [int(x.split("_")[1])
        for x in ticketDetail["rarityList"]
    ]
    extraCloneChar = ticketDetail["extraCharIds"] if ticketDetail.__contains__("extraCharIds") else []
    haveUpgradeBonus = False if recruitTicketId.find("discount") == -1 else True
    rarity6Buff = rogueExtension["upgrade_bonus_6"]
    rarity5Buff = rogueExtension["upgrade_bonus_5"]
    rarity4Buff = rogueExtension["upgrade_bonus_4"]
    rarityALLBuff = rogueExtension["recruit_discount_all"]
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
                rarity = (0 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 1) + (-1 if char["profession"] in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
            case 5:
                rarity = (1 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 2) + (-1 if char["profession"] in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
            case 6:
                rarity = (3 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 3) + (-1 if char["profession"] in upgradeBonusProfessionList else 0)
                if rarity < 0:
                    rarity = 0
            case _:
                rarity = 0
        char.update(
            {
                "type": "NORMAL",
                "upgradeLimited": False,
                "upgradePhase": 1,
                "isUpgrade": True,
                "isCure": False,
                "population": rarity if not isFreeUpgrade else 0,
                "defaultSkillIndex": 0,
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
                rarity = (0 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 2) + isAddPopulationCost + (-2 if rarity4Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0) + (-2 if rarityALLBuff else 0)
                if rarity < 0:
                    rarity = 0
                rarity4Dict[charProfession].append(char)
            case 5:
                rarity = (2 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 3) + isAddPopulationCost + (-2 if rarity5Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0) + (-2 if rarityALLBuff else 0)
                if rarity < 0:
                    rarity = 0
                rarity5Dict[charProfession].append(char)
            case 6:
                rarity = (6 if NEW_RECRUIT_POPULATION_COST_SYSTEM else 6) + isAddPopulationCost + (-2 if rarity6Buff else 0) + (-2 if charProfession in upgradeBonusProfessionList else 0) + (-2 if rarityALLBuff else 0)
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
                "defaultSkillIndex": 0,
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