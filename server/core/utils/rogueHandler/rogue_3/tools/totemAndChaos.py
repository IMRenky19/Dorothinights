from random import shuffle, random, choice
from server.core.utils.json import read_json

from ... import common
from ...common import NodeType
from server.constants import ROGUE_RELIC_POOL_PATH


from ...common.rlv2tools import *

totemPool = read_json(ROGUE_RELIC_POOL_PATH)["rogue_3"]["totemAll"]

def generatePredictPending(rogueData: dict, rogueExtension: dict):
    index = getNextPendingIndex(rogueData)
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
    if rogueExtension["band_12_always_predict_totem"] or getChaosLevel(rogueData) < 3:
        rogueData["current"]["module"]["totem"]["predictTotemId"] = choice(totemPool)
    elif getChaosLevel(rogueData) >= 3:       #TODO:坍缩远见
        rogueData["current"]["module"]["totem"]["predictTotemId"] = choice(totemPool)
        

            
        
        
        
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
        print(currentIndex)
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


def deepenChaos(rogueData: dict, amount: int):
    pass