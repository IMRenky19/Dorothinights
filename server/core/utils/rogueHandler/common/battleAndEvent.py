from sqlalchemy.pool import Pool
from sqlalchemy.util.langhelpers import NoneType
from server.constants import ROGUE_RELIC_POOL_PATH, ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_ROUTE_PATH, ROGUE_EVENT_DETAILS_PATH, ROGUE_BATTLE_POOL_PATH
from random import shuffle, randint, sample, random, choice
from server.core.utils.json import read_json


from .rlv2tools import *
from .map import NodeType

rogueTable: dict = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
roguePoolTable = read_json(ROGUE_RELIC_POOL_PATH)
rogueEventTable = read_json(ROGUE_EVENT_DETAILS_PATH)
rogueBattlePool = read_json(ROGUE_BATTLE_POOL_PATH)


ZONE_1_NORMAL_BATTLE_POOL = []
ZONE_2_NORMAL_BATTLE_POOL = []
ZONE_3_NORMAL_BATTLE_POOL = []
ZONE_4_NORMAL_BATTLE_POOL = []
ZONE_5_NORMAL_BATTLE_POOL = []
ZONE_6_NORMAL_BATTLE_POOL = []






def battleGenerator(mapData: dict, zone: int, pool: list, currentPosition: dict | None) -> dict:
    
    if not currentPosition:
        shuffle(pool)
        for node_position, node in mapData[str(zone)]["nodes"].items():
            if node["pos"]["x"] == 0 and (not node["stage"]):
                if node["realNodeType"] == NodeType.NORMAL_BATTLE:
                    node["type"] = NodeType.NORMAL_BATTLE
                    node["stage"] = pool.pop()
                    pool.insert(0, node["stage"])
                elif node["realNodeType"] == NodeType.ELITE_BATTLE:
                    node["type"] = NodeType.ELITE_BATTLE
                    node["stage"] = pool.pop().replace("ro3_n_", "ro3_e_")
                    pool.insert(0, node["stage"].replace("ro3_e_", "ro3_n_"))
        shuffle(pool)
        return mapData
                
    else:
        shuffle(pool)
        currentNode = mapData[str(zone)]["nodes"][positionToIndex(currentPosition)]
        nextNode = [mapData[str(zone)]["nodes"][positionToIndex(node)] \
            for node in currentNode["next"]]
        #print(nextNode)
        for node in nextNode:
            if not node["stage"]:
                if node["realNodeType"] == NodeType.NORMAL_BATTLE:
                    node["type"] = NodeType.NORMAL_BATTLE
                    #print(pool)
                    node["stage"] = pool.pop()
                    pool.insert(0, node["stage"])
                elif node["realNodeType"] == NodeType.ELITE_BATTLE:
                    node["type"] = NodeType.ELITE_BATTLE
                    node["stage"] = pool.pop().replace("ro3_n_", "ro3_e_")
                    pool.insert(0, node["stage"].replace("ro3_e_", "ro3_n_"))
        shuffle(pool)
        return mapData

def eventGenerator(zone: int, pool: dict, theme: str) -> str:
    if not pool:
        return choice(eventPoolGenerator(zone, [], theme))
    return pool.pop(0)


def battlePoolGenerator(zone: int, theme: str) -> list:
    match zone:
        case 1:
            pool = rogueBattlePool[theme]["ZONE_1_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 2:
            pool = rogueBattlePool[theme]["ZONE_2_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 3:
            pool = rogueBattlePool[theme]["ZONE_3_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 4:
            pool = rogueBattlePool[theme]["ZONE_4_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 5:
            pool = rogueBattlePool[theme]["ZONE_5_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 6:
            pool = rogueBattlePool[theme]["ZONE_6_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        case 7:
            pool = rogueBattlePool[theme]["ZONE_6_NORMAL_BATTLE_POOL"]
            shuffle(pool)
            return pool
        

def eventPoolGenerator(zone: int, currentPool: list, theme: str) -> dict:
    tmpPool = []
    for name, detail in rogueEventTable[theme]["Encounter"]["enterScene"].items():
        if type(detail["zone"]) != list:
            if detail["zone"] == zone:
                tmpPool.append(name)
    shuffle(tmpPool)
    currentPool += tmpPool
    newPool = []
    for name in currentPool:
        pullOut = rogueEventTable[theme]["Encounter"]["enterScene"][name]["pullOut"]
        if pullOut == None:
            pullOut = 114514
        if zone < pullOut:
            newPool.append(name)
    return newPool

def generateBattleBuffs(rogueData: dict, rogueExtension: dict, buffs: list, themeBuffs: list) -> dict:
    modeGrade = getModeGrade(rogueData)
    theme = getTheme(rogueData)
    zone = getCurrentZone(rogueData)
    for i in range(len(themeBuffs)):
        if modeGrade < i:
            break
        for j in themeBuffs[i][1]:
            themeBuffs[j] = ([], [])
    for i in range(len(themeBuffs)):
        if modeGrade < i:
            break
        buffs += themeBuffs[i][0]
    
    for i in range(zone):
        buffs += [
            {
                "key": "global_buff_normal",
                "blackboard": [
                    {
                        "key": "key",
                        "valueStr": "enemy_atk_down"
                    },
                    {
                        "key": "atk",
                        "value": 1 + rogueExtension["difficulty_multiplier"]
                    }
                ]
            },
            {
                "key": "global_buff_normal",
                "blackboard": [
                    {
                        "key": "key",
                        "valueStr": "enemy_max_hp_down"
                    },
                    {
                        "key": "max_hp",
                        "value": 1 + rogueExtension["difficulty_multiplier"]
                    }
                ]
            }
        ]

    for relic in rogueData["current"]["inventory"]["exploreTool"]:
        item_id = rogueData["current"]["inventory"]["exploreTool"][relic]["id"]
        if item_id in rogueTable["details"][theme]["relics"]:
            buffs += rogueTable["details"][theme]["relics"][item_id]["buffs"]
        
    return buffs
    
    
def generateBattlePending(rogueData: dict, rogueExtension: dict, boxInfo: dict, buffs: list, themeBuffs: list) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    battleBuffs = generateBattleBuffs(rogueData, rogueExtension, buffs, themeBuffs)
    
    """boxInfo = {}
    chestCnt = 0
    for i in range(2):
        rd = random()
        if rd <= 0.015:
            chestCnt += 1
            if boxInfo.__contains__("trap_110_smbbox"):
                boxInfo["trap_110_smbbox"] += 1
            else:
                boxInfo["trap_110_smbbox"] = 1
        elif rd <= 0.045:
            chestCnt += 1
            if boxInfo.__contains__("trap_109_smrbox"):
                boxInfo["trap_109_smrbox"] += 1
            else:
                boxInfo["trap_109_smrbox"] = 1
        elif rd <= 0.15:
            chestCnt += 1
            if boxInfo.__contains__("trap_108_smbox"):
                boxInfo["trap_108_smbox"] += 1
            else:
                boxInfo["trap_108_smbox"] = 1"""
    pending = {
        "index":pendingIndex,
        "type":"BATTLE",
        "content":{
            "battle":{
                "state":1,
                "chestCnt":0,
                "goldTrapCnt":0,
                "diceRoll":[],
                "boxInfo":boxInfo,
                "tmpChar":[],
                "sanity":0,
                "unKeepBuff":battleBuffs
            }
        }
    }
    
    return pending

def generateNonBattlePending(pendingIndex: int, currentNodeType: int, rogueData: dict, rogueExtension: dict, selectedChoices = None, goodsList = []) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    currentNodeType = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]["type"]
    theme = getTheme(rogueData)
    match currentNodeType:
        case NodeType.ENCOUNTER | NodeType.ENTERTAINMENT | NodeType.LOST_AND_FOUND | NodeType.WISH | NodeType.SCOUT | NodeType.SAFE_HOUSE | NodeType.STORY | NodeType.PASSAGE:
            if (not rogueData["current"]["player"]["pending"]):
                eventId = eventGenerator(rogueExtension["realZone"], rogueExtension["eventPool"], theme)
                choices = {}
                choiceAdditional = {}
                for eventChoice, eventDetails in rogueEventTable[theme]["Encounter"]["enterScene"][eventId]["choices"].items():
                    choices.update(
                        {
                            eventChoice: 1
                        }
                    ),
                    choiceAdditional.update(
                        {
                            eventChoice: {
                                "rewards":[]
                            }
                        }
                    )
                pending = {
                    "index":pendingIndex,
                    "type":"SCENE",
                    "content":{
                        "scene":{
                            "id":eventId,
                            "choices":choices,
                            "choiceAdditional":choiceAdditional,
                            "independent":False
                        }
                    }
                }
                rogueExtension["currentEvent"] = eventId
                rogueExtension["currentScene"] = eventId
            elif rogueData["current"]["player"]["pending"] and rogueData["current"]["player"]["pending"][0]["type"] == "SCENE":
                #print(114514)
                choices = {}
                choiceAdditional = {}
                nextScene = rogueEventTable[theme]["Encounter"]["others"][getCurrentScene(rogueExtension)]
                if not nextScene:
                    choices = {
                        "choice_leave": 1
                    }
                    choiceAdditional = {
                        "choice_leave": {
                            "rewards":[]
                        }
                    }
                else:
                    for eventChoice, eventDetails in nextScene["choices"].items():
                        choices.update(
                            {
                                eventChoice: 1
                            }
                        ),
                        choiceAdditional.update(
                            {
                                eventChoice: {
                                    "rewards":[]
                                }
                            }
                        )
                pending = {
                    "index":pendingIndex,
                    "type":"SCENE",
                    "content":{
                        "scene":{
                            "id":getCurrentScene(rogueExtension),
                            "choices":choices,
                            "choiceAdditional":choiceAdditional,
                            "independent":False
                        }
                    }
                }
        case NodeType.SHOP:
            zone = getCurrentZone(rogueData)
            if zone == 1:
                shopId = "zone_1_shop"
            else:
                shopId = "zone_6_shop"
            goods = generateShopGoods(shopId, rogueData, rogueExtension, theme)
            pending = {
                "index":pendingIndex,
                "type":"BATTLE_SHOP",
                "content":{
                    "battleShop":{
                        "bank":{
                            "open":True,
                            "canPut":rogueExtension["canShopPut"],
                            "canWithdraw":True,
                            "withdraw":0,
                            "cost":rogueExtension["shopCost"]
                        },
                        "id":shopId,
                        "goods":goodsList,
                        "canBattle":not rogueExtension["shopHaveBattled"],
                        "hasBoss":not rogueExtension["shopHaveBattled"],
                        "refreshCnt":rogueExtension["refresh_shop"],
                        "showRefresh":True if rogueExtension["refresh_shop"]else False,
                        "withdrawMethod":"fee_add",
                        "refreshMethod":"direct",
                        "_done":False
                    }
                }
            }
    
    return pending

def generateBattleRewardPending(rogueData: dict, rogueExtension: dict, stageName: str, stageType: int, decryptedBattleData: dict, theme: str, rewards = [], gainExp = 0) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    
    lastHp = decryptedBattleData["battleData"]["stats"]["leftHp"]
    battleStats = decryptedBattleData["battleData"]["stats"]["charStats"]
    
    
    """for item in battleStats:
        if item["Key"]["charId"] == "trap_108_smbox" and item["Key"]["counterType"] == "DEAD":
            normalBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_109_smrbox" and item["Key"]["counterType"] == "DEAD":
            rareBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_110_smbbox" and item["Key"]["counterType"] == "DEAD":
            superRareBoxCount += item["Value"]"""
            
    
    addInfo = addExp(rogueData, gainExp)
    if addInfo["hpLimit"]:
        lastHp += addInfo["hpLimit"]
    
    if lastHp <= getHp(rogueData):
        gainShield = -getShield(rogueData)
        damageHp = getHp(rogueData) - lastHp
    else:
        gainShield = -(getHp(rogueData) + getShield(rogueData) - lastHp)
        damageHp = 0
        
    pending = {
        "index":pendingIndex,
        "type":"BATTLE_REWARD",
        "content":{
            "battleReward": {
                "earn": {
                    "damage": damageHp,
                    "hp": -damageHp,
                    "shield": gainShield,
                    "exp": gainExp,
                    "populationMax": addInfo["population"],
                    "squadCapacity": addInfo["capacity"],
                    "maxHpUp": addInfo["hpLimit"]
                },
                "rewards": [],
                "show": "1"
            }
        }
    }
    
    
    pending["content"]["battleReward"]["rewards"] = rewards
    pending["content"]["battleReward"]["show"] = randint(0, len(rogueData["current"]["troop"]["chars"]) - 1) if rogueData["current"]["troop"]["chars"] else 0
    addShield(rogueData, gainShield)
    addHp(rogueData, -damageHp)
    return pending



def generateBaseBattleRewards(stage: str, isElite: bool, isBoss: bool, gainGold: int, chestInfo: dict, theme: str, chanceInfo: dict, ticketCount = 1, rogueExtension: dict = {}, hasRelicInfo: dict = {}, rogueData = {}) -> list:
    index = 0
    rewards = []
    #TODO:根据是否在树洞更改部分资源掉落概率
    relicChance = chanceInfo["relicChance"]["isElite"] if isElite else chanceInfo["relicChance"]["notElite"]
    if isBoss:
        relicChance = 1
    """visionChance = chanceInfo[""]
    totemChance = chanceInfo[""] if isElite else chanceInfo[""]"""
    
    #掉落顺序1：原石锭
    rewards.append(
        {
            "index": index,
            "items":[
                {
                    "sub": 0,
                    "id": f"{theme}_gold",
                    "count":gainGold
                }
            ],
            "done": 0
        }
    )
    index += 1
    if nmrBox := chestInfo["normalBox"]:
        for i in range(nmrBox):
            rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_gold",
                        "count":2
                    }
                ],
                "done": 0,
                "exDrop": 1
                }
            )
            index += 1
    if rareBox := chestInfo["rareBox"]:
        for i in range(rareBox):
            rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_gold",
                        "count":4
                    }
                ],
                "done": 0,
                "exDrop": 1
                }
            )
            index += 1
    if superRareBox := chestInfo["superRareBox"]:
        for i in range(superRareBox):
            rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_gold",
                        "count":10
                    }
                ],
                "done": 0,
                "exDrop": 1
                }
            )
            index += 1
            
    #TODO 掉落顺序2：藏品
    #TODO 根据难度不同进阶部分藏品，部分藏品的即时效果生效（chooseBattleReward）
    hasRelicInfo = rogueData["current"]["inventory"]["relic"]
    hasRelic = [x["id"] for x in hasRelicInfo.values()]
    relics = [i for i in roguePoolTable[theme]["battleRelicPool"] if not (i in hasRelic)] if not isBoss else [i for i in roguePoolTable[theme]["bossRelicPool"] if not (i in hasRelic)]
    relicCount = 2 if isBoss else 1
    sub = 0
    relicItems = []
    if random() < relicChance:
        for i in range(relicCount):
            relic = relicLevelCheck(relics.pop(randint(0,len(relics) - 1)), rogueExtension)
            relicItems.append(
                {
                    "sub": i,
                    "id": relic,
                    "count": 1
                }
            )
            sub += 1
        rewards.append(
            {
            "index": index,
            "items":relicItems,
            "done": 0
            }
        )
        index += 1
        
    #掉落顺序3：招募券
    if isElite:
        upgradeChance = 0.5
    if isBoss:
        upgradeChance = 1
    else:
        upgradeChance = 0
        
    ticketBaseObject = {
                "index": index,
                "items":[],
                "done": 0
            }
    for i in range(ticketCount):
        ticketBaseObject["items"].append(
            {
                "sub": i,
                "id": 0,
                "count": 1
            }
        )
    
    generateTickets(ticketBaseObject, upgradeChance, theme)
    rewards.append(ticketBaseObject)
    index += 1
    return {
        "rewards": rewards,
        "lastIndex": index,
        "relicPool": relics
    }
        

def gainItemsAfterBattle(rogueData: dict, index: int, subIndex: int, userData = None, rogueExtension = None):
    theme = getTheme(rogueData)
    #TODO 招募券以及典训藏品的激活，部分加携带/生命值/护盾/希望等等的资源增加，部分藏品的特殊效果（密信系列的招募减希望/直升，和坍缩值/指挥经验相关机制，叠层藏品）
    battleRewardsPending = rogueData["current"]["player"]["pending"]
    itemType: str = battleRewardsPending[-1]["content"]["battleReward"]["rewards"][index]["items"][subIndex]["id"]
    itemCount = battleRewardsPending[-1]["content"]["battleReward"]["rewards"][index]["items"][subIndex]["count"]
    item = battleRewardsPending[-1]["content"]["battleReward"]["rewards"][index]
    gainItem(rogueData, itemType, itemCount, userSyncData = userData, rogueExtension=rogueExtension)
    item["done"] = 1
        
def gainItem(rogueData: dict, itemType: str, amount: int, item: str = None, userSyncData = None, rogueExtension = None, canUpgradeIndex = None):
    theme = getTheme(rogueData)
    if not itemType:
        itemType = item
    #if len(itemType.split('_')) == 1:
    #    itemType = itemType.split('_')[2]
    match itemType:
        case itemType if itemType.find("gold") != -1:
            addGold(rogueData, amount)
        case itemType if itemType.find("_ticket") != -1:
            for i in range(int(amount)):
                ticketId = addTicketBattle(rogueData, item)
            activateTickets(rogueData, item if item else itemType, userSyncData, rogueExtension, ticketId)
        case itemType if itemType.find("relic") != -1:
            realRelic = relicLevelCheck(item, rogueExtension)
            index = addRelic(rogueData, realRelic)
            processRelic(rogueData, rogueExtension, index, userSyncData)
        case itemType if itemType.find("shield") != -1:
            addShield(rogueData, amount)
        case itemType if itemType.find("population") != -1:
            addPopulation(rogueData, amount)
        case itemType if itemType.find("hpmax") != -1:
            addHpLimit(rogueData, amount)
        case itemType if itemType.find("hp") != -1:
            addHp(rogueData, amount)
        case itemType if itemType.find("explore_tool") != -1:     #深入调查
            pass
        case itemType if itemType.find("active_tool") != -1:        #支援装置       
            index = addRelic(rogueData, item)
        case itemType if itemType.find("capacity") != -1:
            addCapacity(rogueData, amount)
        case itemType if itemType.find("char_limit") != -1:
            #addCharLimit(rogueExtension, amount)
            pass
        case itemType if itemType.find("totem") != -1:
            addTotem(rogueData, itemType)
        case itemType if itemType.find("vision") != -1:
            addVision(rogueData, amount)
        case itemType if itemType.find("chaos") != -1:
            addChaos(rogueData, amount)
           
def activateTickets(rogueData: dict, item, userSyncData, rogueExtension, ticketId):
    theme = getTheme(rogueData)
    addRecruitPending(rogueData, ticketId)
    chars = getChars(
        rogueData, 
        rogueExtension, 
        item, 
        userSyncData
    )
    rogueData["current"]["inventory"]["recruit"][ticketId]["state"] = 1
    rogueData["current"]["inventory"]["recruit"][ticketId]["list"] = chars
    
def processRelic(rogueData, rogueExtension, index, userSyncData):
    theme = getTheme(rogueData)
    relicId = rogueData["current"]["inventory"]["relic"][index]["id"]
    relicDetail = rogueTable["details"][theme]["relics"][relicId]
    for buff in relicDetail["buffs"]:
        if buff["key"] == "immediate_reward":
            gainItem(rogueData, buff["blackboard"][0]["valueStr"], buff["blackboard"][1]["value"], buff["blackboard"][0]["valueStr"], userSyncData, rogueExtension)
        if buff["key"] == "immediate_cost":
            gainItem(rogueData, buff["blackboard"][0]["valueStr"], -(buff["blackboard"][1]["value"]), buff["blackboard"][0]["valueStr"], userSyncData, rogueExtension)
    
def relicLevelCheck(relicId: str, rogueExtension: dict):
    canUpgradeIndex = rogueExtension["canUpgradeIndex"]
    realRelic = relicId
    tmp = relicId.split("_")
    if tmp[3] == "legacy" and int(tmp[4]) in canUpgradeIndex:
        match rogueExtension["stronger_relics"]:
            case 1:
                if len(tmp) == 6:
                    tmp[5] = "a"
                    realRelic = "_".join(tmp)
                else:
                    tmp.append("a")
                    realRelic = "_".join(tmp)
            case 2:
                if len(tmp) == 6:
                    tmp[5] = "b"
                    realRelic = "_".join(tmp)
                else:
                    tmp.append("b")
                    realRelic = "_".join(tmp)
            case 3:
                if len(tmp) == 6:
                    tmp[5] = "c"
                    realRelic = "_".join(tmp)
                else:
                    tmp.append("c")
                    realRelic = "_".join(tmp)
            case 0:
                realRelic = "_".join(tmp[:5])
    return realRelic
    
def generateTickets(ticketBaseObject: dict, upgradeChance: float, theme: str):
    ticketPool = [
        f"{theme}_recruit_ticket_pioneer",
        f"{theme}_recruit_ticket_warrior",
        f"{theme}_recruit_ticket_tank",
        f"{theme}_recruit_ticket_sniper",
        f"{theme}_recruit_ticket_caster",
        f"{theme}_recruit_ticket_support",
        f"{theme}_recruit_ticket_medic",
        f"{theme}_recruit_ticket_special"
    ]
    upgradePool: list = [
        f"{theme}_recruit_ticket_all_premium",
        f"{theme}_recruit_ticket_all_discount",
        f"{theme}_upgrade_ticket_all"
    ]
    pioneer_and_warrior_pool = [
        f"{theme}_recruit_ticket_quad_melee_discount",
        f"{theme}_recruit_ticket_double_1"
    ]
    tank_and_support_pool = [
        f"{theme}_recruit_ticket_double_2"
    ]
    sniper_and_medic_pool = [
        f"{theme}_recruit_ticket_quad_ranged_discount",
        f"{theme}_recruit_ticket_double_3"
    ]
    caster_and_special_pool = [
        f"{theme}_recruit_ticket_double_4"
    ]
    allProfession = True
    for item in ticketBaseObject["items"]:
        item["id"] = choice(ticketPool)
        ticketPool.pop(ticketPool.index(item["id"]))
        match item["id"][23:]:
            case "pioneer" | "warrior":
                if random() < upgradeChance and pioneer_and_warrior_pool:
                    item["id"] = pioneer_and_warrior_pool.pop()
                    if allProfession and random() < 0.3:
                        item["id"] = choice([upgradePool])
                        allProfession = False
            case "tank" | "support":
                if random() < upgradeChance and tank_and_support_pool:
                    item["id"] = tank_and_support_pool.pop()
                    if allProfession and random() < 0.3:
                        item["id"] = choice([upgradePool])
                        allProfession = False
            case "sniper" | "medic":
                if random() < upgradeChance and sniper_and_medic_pool:
                    item["id"] = sniper_and_medic_pool.pop()
                    if allProfession and random() < 0.3:
                        item["id"] = choice([upgradePool])
                        allProfession = False
            case "caster" | "special":
                if random() < upgradeChance and caster_and_special_pool:
                    item["id"] = caster_and_special_pool.pop()
                    if allProfession and random() < 0.3:
                        item["id"] = choice([upgradePool])
                        allProfession = False
    
    
