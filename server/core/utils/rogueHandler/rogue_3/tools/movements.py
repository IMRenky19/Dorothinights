from server.core.utils.rogueHandler.common.map import NodeType
from server.core.utils.time import time
from ...common.rlv2tools import *
from ... import common
from .map import mapGenerator
from .battleAndEvent import battleGenerator, gainItem
from .totemAndChaos import *
from .visionProcessor import *
from server.constants import ROGUE_RELIC_POOL_PATH

totemList = read_json(ROGUE_RELIC_POOL_PATH)["rogue_3"]["totemAll"]


ts = time()


def moveToNextZone(rlv2_data: dict, rlv2_extension: dict, userSyncData, isHiddenZone = False):
    retval = common.moveToNextZone(rlv2_data, rlv2_extension)
    zone = getCurrentZone(rlv2_data)
    battlePool = retval[0]
    #萨米肉鸽额外处理
    mapData = battleGenerator(
        visionGenerator(
            rlv2_data["current"]["player"]["cursor"]["zone"],
            getPosition(rlv2_data),
            getVision(rlv2_data),
            mapGenerator(
                zone, 
                getNextZoneId(rlv2_data), 
                alternativeBoss=True,
            )
        ),
        zone,
        battlePool,
        getPosition(rlv2_data),
        False,
        []
    )
    rlv2_data["current"]["map"]["zones"].update(mapData)
    if rlv2_extension["3_add_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] == 3:
        addVision(rlv2_data, 1, rlv2_extension) 
    if rlv2_data["current"]["player"]["cursor"]["zone"] == 1:
        if rlv2_extension["band_13_another_vision_set"]:
            setVision(rlv2_data, 0)
        else:
            setVision(rlv2_data, 3)
    if rlv2_extension["band_13_another_vision_set"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (2, 3, 4, 5, 6):
        addVision(rlv2_data, 2, rlv2_extension)
    if rlv2_extension["12_less_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (1,3,5):
        addVision(rlv2_data, -1, rlv2_extension)
    if not isHiddenZone:
        if rlv2_data["current"]["module"]["totem"]["predictTotemId"]:
            addTotem(rlv2_data, rlv2_data["current"]["module"]["totem"]["predictTotemId"])
        generatePredictPending(rlv2_data, rlv2_extension)
        
    #测试密文版
    if zone == 1:
        for totem in totemList:
            gainItem(rlv2_data, totem, 1, totem, userSyncData, rogueExtension=rlv2_extension)
    if not isHiddenZone:
        chaosList = [0,3,4,5,6,7] if rlv2_extension["15_more_chaos"] else [0,3,3,3,3,3]
        #increaseChaosValue(rlv2_data, rlv2_extension, chaosList[zone - 1], True)
        increaseChaosValue(rlv2_data, rlv2_extension, 15, True)
    
    
def moveTo(rlv2_data: dict, rlv2_extension: dict, position: dict, zone: int):
    currentPosition = getPosition(rlv2_data)
    common.moveTo(rlv2_data, rlv2_extension, position, zone) 
    currentVision = getVision(rlv2_data)
    gainRandomItems = False
    
    if currentPosition:
        if currentPosition["x"] == position["x"]:
            if not isRelicExist(rlv2_data, "rogue_3_relic_explore_3", rlv2_extension):
                addVision(rlv2_data, -1, rlv2_extension)
            else:
                if random() > 0.3:
                    addVision(rlv2_data, -1, rlv2_extension)
            if currentVision <= 1 and isRelicExist(rlv2_data, "rogue_3_relic_res_10", rlv2_extension):
                gainRandomItems = True if random() >= 0.5 else False
        else:
            if currentVision <= 1 and isRelicExist(rlv2_data, "rogue_3_relic_res_10", rlv2_extension):
                gainRandomItems = True if random() >= 0.5 else False
                
    if gainRandomItems:
        rd = random()
        if rd < 0.5:
            rd2 = choice([1,2,3])
            if rd2 == 1:
                addShield(rlv2_data, 1)
            if rd2 == 2:
                addGold(rlv2_data, 1)
            if rd2 == 3:
                addPopulation(rlv2_data, 1)
        elif rd < 0.8:
            addVision(rlv2_data, 1, rlv2_extension)
        else:
            totem = choice(totemList)
            addTotem(rlv2_data, totem)
            rlv2_extension["extraResponse"] = {
                "items": [
                    {
                        "id": totem,
                        "count": 1
                    }
                ]
            }
            rlv2_extension["isNewExtraResponse"] = True
    
    rlv2_data["current"]["map"]["zones"].update(
        battleGenerator(
            visionGenerator(
                rlv2_data["current"]["player"]["cursor"]["zone"],
                getPosition(rlv2_data),
                getVision(rlv2_data),
                rlv2_data["current"]["map"]["zones"]
            ),
            rlv2_data["current"]["player"]["cursor"]["zone"],
            rlv2_extension["battlePool"],
            rlv2_data["current"]["player"]["cursor"]["position"],
            False,
            []
        )
    )
    
    
def zoneEndChecker(rogueData: dict, rogueExtensionData: dict, userSyncData: dict):
    if isZoneEnd(rogueData):
        if getCurrentZone(rogueData) == 5:
            endGame(rogueData, rogueExtensionData)
            return
        moveToNextZone(rogueData, rogueExtensionData, userSyncData)
        
        
def endGame(rogueData: dict, rogueExtensionData: dict):
    index = getNextPendingIndex(rogueData)
    success = 1
    ts = time()
    normalBattleCount = 0
    eliteBattleCount = 0
    bossCount = 0
    
    zoneCount = len(rogueData["current"]["map"]["zones"].keys())
    zoneList = []
    for index, zone in rogueData["current"]["map"]["zones"].items():
        zoneList.append({
                "index":zone["index"],
                "zoneId":zone["id"],
                "variation": []     #TODO
            }
        )
    
    totemList = []
    for totem in rogueData["current"]["module"]["totem"]["totemPiece"]:
        totemList.append(totem["id"])
    
    for traceNode in rogueData["current"]["player"]["trace"]:
        nodeType = rogueData["current"]["map"]["zones"][str(traceNode["zone"])]["nodes"][positionToIndex(traceNode["position"])]["type"]
        match nodeType:
            case NodeType.NORMAL_BATTLE:
                normalBattleCount += 1
            case NodeType.ELITE_BATTLE:
                eliteBattleCount += 1
            case NodeType.BOSS:
                bossCount += 1
    
    stepCount = len(rogueData["current"]["player"]["trace"])
    itemCount = len(rogueData["current"]["inventory"]["relic"].keys())
    if rogueData["current"]["inventory"]["trap"]:
        itemCount += len(rogueData["current"]["inventory"]["trap"].keys())
        
    recruitCount = len([x for x in rogueData["current"]["inventory"]["recruit"].values() if x["from"] != "initial"])
    #upgradeCount = 暂缓.jpg
    
    troopChars = []
    for index, char in rogueData["current"]["troop"]["chars"].items():
        troopChars.append({
            "instId":str(int(index) + 1),
            "charId":char["charId"],
            "type":char["type"],
            "upgradePhase":char["upgradePhase"],
            "evolvePhase":char["evolvePhase"],
            "level":char["level"]
        })
    
    relicList = [x["id"] for x in rogueData["current"]["inventory"]["relic"].values()]
    relicList.pop(0)
    activeToolList = []
    if rogueData["current"]["inventory"]["trap"]:
        activeToolList = [x["id"] for x in rogueData["current"]["inventory"]["trap"].values()]
    
    brief = {
                    "level":getHardLevel(rogueData),
                    "over":True,
                    "success":success,
                    "ending":getToEnding(rogueData),
                    "theme":"rogue_3",
                    "mode":"NORMAL",
                    "predefined":None,
                    "band":getBand(rogueData),
                    "startTs":getStartTs(rogueData),
                    "endTs":ts,
                    "endZoneId":f"zone_{getCurrentZone(rogueData)}",
                    "endProperty":{
                        "hp":getHp(rogueData),
                        "gold":getGold(rogueData),
                        "populationCost":getPopulationCost(rogueData),
                        "populationMax":getPopulationMax(rogueData),
                        "vision":getVision(rogueData),
                        "chaos":getChaos(rogueData)
                    },
                    "innerMission":False,
                    "innerMissionProcess":None,
                    "innerMissionProcessAddition":None,
                    "modeGrade":getHardLevel(rogueData)
                }
    pending = {
        "index":index,
        "type":"GAME_SETTLE",
        "content":{
            "success": success,
            "result": {
                "brief": brief,
                "record": {
                    "cntZone":zoneCount,
                    "cntBattleNormal":normalBattleCount,
                    "cntBattleElite":eliteBattleCount,
                    "cntBattleBoss":bossCount,
                    "cntArrivedNode":stepCount,
                    "cntRecruitChar":0,
                    "cntUpgradeChar":0,
                    "cntKillEnemy":0,
                    "cntShopBuy":0,
                    "cntPerfectBattle":0,
                    "cntProtectBox":0,
                    "cntRecruitFree":0,
                    "cntRecruitAssist":0,
                    "cntRecruitNpc":0,
                    "cntRecruitProfession":{
                        "SPECIAL":0,
                        "SNIPER":0,
                        "PIONEER":0,
                        "WARRIOR":0,
                        "CASTER":0,
                        "MEDIC":0,
                        "TANK":0,
                        "SUPPORT":0
                    },
                    "recruitRealCount": recruitCount,
                    "troopChars": troopChars,
                    "itemCount": itemCount - 1,
                    "cntArrivedNodeType":{      #TODO
                        "BATTLE_NORMAL":0,
                        "BATTLE_SHOP":0,
                        "PORTAL":0,
                        "BATTLE_ELITE":0,
                        "EXPEDITION":0,
                        "WISH":0,
                        "REST":0,
                        "INCIDENT":0,
                        "STORY_HIDDEN":0,
                        "BATTLE_BOSS":0,
                        "SACRIFICE":0,
                        "STORY":0,
                        "ENTERTAINMENT":0
                    },
                    "relicList": relicList,
                    "capsuleList":[],
                    "activeToolList":activeToolList,
                    "exploreToolList":[],
                    "zones":zoneList,
                    "nodeMission": {},
                    "totemList": totemList
                }
                
            }
        },
        "detailStr": None,  #TODO
        "popReport": False
    }
    rogueData["current"]["record"]["brief"] = brief
    clearAllPending(rogueData)
    addPending(rogueData, pending)
    
    
    