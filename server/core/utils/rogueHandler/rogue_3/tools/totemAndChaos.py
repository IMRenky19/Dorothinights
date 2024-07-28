from random import shuffle, random, choice

from server.core.utils.json import read_json

from server.constants import ROGUE_RELIC_POOL_PATH, ROGUE_MODULE_DATA_PATH


from ...common.rlv2tools import *

totemPool = read_json(ROGUE_RELIC_POOL_PATH)["rogue_3"]["totemAll"]
chaosPool = read_json(ROGUE_MODULE_DATA_PATH)["rogue_3"]["chaos"]

def getChaos(rlv2_data: dict):
    return rlv2_data["current"]["module"]["chaos"]["chaosList"]

def addChaos(rlv2_data: dict, add: int):
    rlv2_data["current"]["module"]["chaos"]["value"] += add
    if rlv2_data["current"]["module"]["chaos"]["value"] < 0:
        rlv2_data["current"]["module"]["chaos"]["value"] = 0
    
def setChaos(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["chaos"]["value"] = sets

def setChaosMaxValue(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["chaos"]["curMaxValue"] = sets
    
def addChaosMaxValue(rlv2_data: dict, add: int):
    rlv2_data["current"]["module"]["chaos"]["curMaxValue"] += add
    
def setChaosMaxLevel(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["chaos"]["level"] = sets
    
def addChaosMaxLevel(rlv2_data: dict, add: int):
    rlv2_data["current"]["module"]["chaos"]["level"] += add
    
def getChaosValue(rlv2_data: dict):
    return rlv2_data["current"]["module"]["chaos"]["value"]

def getChaosLevel(rlv2_data: dict):
    return rlv2_data["current"]["module"]["chaos"]["level"]

def generatePredictPending(rogueData: dict, rogueExtension: dict):
    index = getNextPendingIndex(rogueData)
    if rogueExtension["band_12_always_predict_totem"] or getChaosLevel(rogueData) < 3:
        rogueData["current"]["module"]["totem"]["predictTotemId"] = choice(totemPool)
    elif getChaosLevel(rogueData) >= 3:       #TODO:坍缩远见
        if getChaosLevel(rogueData) >= 8:
            return
        deepenChaos(rogueData, rogueExtension, 0, 1, False, True)
    setCurrentState(rogueData, "PENDING")
    pending = {
        "index": index,
        "type":"PREDICT",
        "content": {
            "predict":{
            }
        }
    }
    addPending(rogueData, pending)
        

            
        
        
        
def getReachableNodeDict(rogueData: dict):
    zoneId = getCurrentZone(rogueData)
    currentPos = getPosition(rogueData)
    allNodeList: dict = deepcopy(rogueData["current"]["map"]["zones"][str(zoneId)]["nodes"])
    if not currentPos:
        return allNodeList
    for nodePos in [x for x in rogueData["current"]["player"]["trace"] if x["zone"] == zoneId]:
        if positionToIndex(nodePos["position"]) != positionToIndex(currentPos):
            allNodeList.pop(positionToIndex(nodePos["position"]))
    
    if currentPos:
        currentIndex = str(positionToIndex(currentPos))
    else:
        currentIndex = None
    reachableNodeDict = {}
    
    
    def tmp(allNodeList: dict, currentIndex, reachableNodeDict):
        if not currentIndex:
            return allNodeList
        nextNode = allNodeList[currentIndex]["next"] if currentIndex else [allNodeList[positionToIndex(x["pos"])] for x in allNodeList.values() if x["pos"]["x"] == 0]
        if currentIndex:
            allNodeList.pop(currentIndex)
        for pos in nextNode:
            posIndex = str(positionToIndex(pos))
            if allNodeList.__contains__(posIndex):
                reachableNodeDict[posIndex] = allNodeList[posIndex]
                if allNodeList[posIndex]["next"]:
                    tmp(allNodeList, posIndex, reachableNodeDict)
                
    tmp(allNodeList, currentIndex, reachableNodeDict)
    return reachableNodeDict

def increaseChaosValue(rogueData: dict, rogueExtension: dict, amount: int, isNewZone = False):
    oldChaosValue = getChaosValue(rogueData)
    addChaos(rogueData, amount)
    if amount > 0 and isRelicExist(rogueData, "rogue_3_relic_legacy_41", rogueExtension, 1):
        addGold(rogueData, 1)
    deepenChaos(rogueData, rogueExtension, oldChaosValue, oldChaosValue + amount, isNewZone)

def chaosLevelChecker(rogueData: dict, rogueExtension: dict) -> int:
    currentChaos = getChaosValue(rogueData)
    currentChaosLevel = getChaosLevel(rogueData)
    normalChaos = [0,4,8,12,16,20,24,28,32,999]
    deeperChaos = [0,4,8,12,15,18,21,23,25,999]
    chaosNumList = deeperChaos if rogueExtension["1_chaos_deeper"] else normalChaos
    chaoticNum = 0
    for i in range(len(normalChaos)):
        if chaosNumList[i] <= currentChaos and chaosNumList[i+1] > currentChaos:
            setChaosMaxLevel(rogueData, i)
            finalChaosLevel = i
            setChaosMaxValue(rogueData, chaosNumList[i+1])
            return finalChaosLevel - currentChaosLevel
    return 0

def deepenChaos(rogueData: dict, rogueExtension: dict, beforeChaos: int, afterChaos: int, isNewZone = False, onlyPredict: bool = False):
    currentChaosList = deepcopy(rogueData["current"]["module"]["chaos"]["chaosList"])
    deltaChaosValue = afterChaos - beforeChaos
    canUpgradeChaos = []
    maxChaosSlot = 4
    waitToProcess = []
    normalChaosList = [x for x in list(chaosPool["normalChaos"].keys()) if not(x in currentChaosList)]
    deeperChaosList = list(chaosPool["deeperChaos"].keys())
    index = 0
    deepenAmount = 0
    currentNormalChaos = []
    currentDeeperChaos = []
    preLevel = 0
    chaosNum = 0
    afterLevel = 0
    if deltaChaosValue > 0:      #加深坍缩
        preLevel = getChaosLevel(rogueData)
        chaosNum = chaosLevelChecker(rogueData, rogueExtension)
        afterLevel = getChaosLevel(rogueData)
        if onlyPredict:
            chaosNum = 1
        for chaos in currentChaosList:
            if len(chaos.split("_")) == 4:
                currentNormalChaos.append(chaos)
            if len(chaos.split("_")) == 5:
                currentDeeperChaos.append(chaos)
        for i in range(chaosNum):
            #某个坍缩概率进阶
            rdNum = random()
            if rdNum == 0:
                rdNum = 1
            if rogueData["current"]["module"]["chaos"].__contains__("predict"):
                if len(rogueData["current"]["module"]["chaos"]["predict"].split("_")) == 4:
                    waitToProcess.append({
                        "operation": "DEEPEN",
                        "chaosId": rogueData["current"]["module"]["chaos"]["predict"]
                    })
                    currentNormalChaos.append(rogueData["current"]["module"]["chaos"]["predict"])
                    rogueData["current"]["module"]["chaos"].pop("predict")
                elif len(rogueData["current"]["module"]["chaos"]["predict"].split("_")) == 5:
                    waitToProcess.append({
                        "operation": "UPGRADE",
                        "chaosId": rogueData["current"]["module"]["chaos"]["predict"]
                    })
                    currentNormalChaos.remove(chaosPool["deeperChaos"][rogueData["current"]["module"]["chaos"]["predict"]]["normalChaosId"])
                    currentDeeperChaos.append(rogueData["current"]["module"]["chaos"]["predict"])
                    rogueData["current"]["module"]["chaos"].pop("predict")
                    
            elif rdNum < ((len(currentNormalChaos) / maxChaosSlot) + (len(currentDeeperChaos) / maxChaosSlot)) and currentNormalChaos:
                rd = choice(currentNormalChaos)
                for operation in waitToProcess:
                    if operation["chaosId"] == rd:
                        waitToProcess.remove(operation)
                waitToProcess.append({
                    "operation": "UPGRADE",
                    "chaosId": chaosPool["normalChaos"][rd]["deeperChaosId"]
                })
                currentNormalChaos.remove(rd)
                currentDeeperChaos.append(chaosPool["normalChaos"][rd]["deeperChaosId"])
                
            else:
                shuffle(normalChaosList)
                new = normalChaosList.pop()
                
                waitToProcess.append({
                    "operation": "DEEPEN",
                    "chaosId": new
                })
                currentNormalChaos.append(new)
                deepenAmount += 1
    if deltaChaosValue < 0: #减轻坍缩
        preLevel = getChaosLevel(rogueData)
        chaosNum = -chaosLevelChecker(rogueData, rogueExtension)
        
        afterLevel = getChaosLevel(rogueData)
        for chaos in currentChaosList:
            if len(chaos.split("_")) == 4:
                currentNormalChaos.append(chaos)
            if len(chaos.split("_")) == 5:
                currentDeeperChaos.append(chaos)
        for i in range(chaosNum):
            #某个坍缩概率弱化
            shuffle(currentChaosList)
            luckyChaos = currentChaosList.pop()
            if len(luckyChaos.split("_")) == 4:
                if rogueData["current"]["module"]["chaos"].__contains__("predict"):
                    if chaosPool["deeperChaos"][rogueData["current"]["module"]["chaos"]["predict"]]["normalChaosId"] == luckyChaos:
                        rogueData["current"]["module"]["chaos"].pop("predict")
                        rogueData["current"]["module"]["chaos"]["predict"] = luckyChaos
                waitToProcess.append(
                {
                        "operation": "DELETE",
                        "chaosId": luckyChaos
                    }
                )
            elif len(luckyChaos.split("_")) == 5:
                waitToProcess.append({
                    "operation": "RELIEVE",
                    "chaosId": chaosPool["deeperChaos"][luckyChaos]["normalChaosId"]
                })
    if deltaChaosValue == 0:
        return
    deepenChangeList = []
    relieveChangeList = []
    for operation in waitToProcess:
        match operation["operation"]:
            case "DEEPEN":
                if onlyPredict:
                    rogueData["current"]["module"]["chaos"]["predict"] = operation["chaosId"]
                    return
                else:
                    rogueData["current"]["module"]["chaos"]["chaosList"].append(operation["chaosId"])
                    deepenChangeList.append(operation["chaosId"])
                
            case "UPGRADE":
                if onlyPredict:
                    rogueData["current"]["module"]["chaos"]["predict"] = operation["chaosId"]
                    return
                elif chaosPool["deeperChaos"][operation["chaosId"]]["normalChaosId"] in rogueData["current"]["module"]["chaos"]["chaosList"]:
                    index = rogueData["current"]["module"]["chaos"]["chaosList"].index(chaosPool["deeperChaos"][operation["chaosId"]]["normalChaosId"])
                    rogueData["current"]["module"]["chaos"]["chaosList"][index] = operation["chaosId"]
                else:
                    rogueData["current"]["module"]["chaos"]["chaosList"].append(operation["chaosId"])
                deepenChangeList.append(operation["chaosId"])
            case "RELIEVE":
                index = rogueData["current"]["module"]["chaos"]["chaosList"].index(chaosPool["normalChaos"][operation["chaosId"]]["deeperChaosId"])
                rogueData["current"]["module"]["chaos"]["chaosList"][index] = operation["chaosId"]
                relieveChangeList.append(chaosPool["normalChaos"][operation["chaosId"]]["deeperChaosId"])
            case "DELETE":
                rogueData["current"]["module"]["chaos"]["chaosList"].remove(operation["chaosId"])
                relieveChangeList.append(operation["chaosId"])
    if (not isNewZone) and deepenChangeList:
        writeExtraResponseData(
            rogueData, 
            rogueExtension, 
            {
                "pushMessage":[
                    {
                        "path":"rlv2ChaosChange",
                        "payload":{
                            "upgrade":True,
                            "changeList":deepenChangeList
                        }
                    }
                ]
            }
        )
    else:
        rogueData["current"]["module"]["chaos"]["deltaChaos"].update(
            {
                "preLevel": preLevel,
                "afterLevel" :afterLevel,
                "dValue": deltaChaosValue, 
                "dChaos": deepenChangeList
            }
        )
        rogueExtension["newZoneChaos"] = True
    if (not isNewZone) and relieveChangeList:
        writeExtraResponseData(
            rogueData, 
            rogueExtension, 
            {
                "pushMessage":[
                    {
                        "path":"rlv2ChaosChange",
                        "payload":{
                            "upgrade":False,
                            "changeList":deepenChangeList
                        }
                    }
                ]
            }
        )