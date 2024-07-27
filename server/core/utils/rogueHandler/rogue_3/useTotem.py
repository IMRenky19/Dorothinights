from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from .. import common
from .tools.battleAndEvent import *
from .tools.movements import *
from .tools.totemAndChaos import increaseChaosValue
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_MODULE_DATA_PATH
from server.core.utils.time import time
from random import shuffle, randint
from ....database.function.userData import getAccountBySecret
import re

ts = time()
rogueExcel = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
rogueModuleData = read_json(ROGUE_MODULE_DATA_PATH)

async def useTotem(rogueClass: RogueBasicModel, totemIndex: list, nodeIndex: list):
    rlv2Data = getRogueData(rogueClass)
    rlv2ExtensionData = getRogueExtensionData(rogueClass)
    user = await getAccountBySecret(rogueClass.secret)
    userSyncData = user.user
    
    increaseChaosValue(rlv2Data, rlv2ExtensionData, -1, False)
    totemList = getTotemList(rlv2Data)
    
    upperTotemId = totemList[int(totemIndex[0].split("_")[1])]["id"]
    lowerTotemId = totemList[int(totemIndex[1].split("_")[1])]["id"]
    
    reachableNodeIdDict = getReachableNodeDict(rlv2Data)
    
    upperTotemData = rogueModuleData["rogue_3"]["totem"]["upper"][upperTotemId]
    lowerTotemData = rogueModuleData["rogue_3"]["totem"]["lower"][lowerTotemId]
    
    if (upperTotemData["type"] == lowerTotemData["type"]) or (upperTotemData["type"] == "ALL"):
        extraEffect = True
    else:
        extraEffect = False
    
    zone = str(getCurrentZone(rlv2Data))
    currentPos = getPosition(rlv2Data)
    if not (zone in [1,2,3,4,5,6,7]):   #TODO
        isHiddenZone = True
    else:
        isHiddenZone = False
        
    #上板：判定范围
    selectedNodeDict = {}
    selectedNodePos = []
    if upperTotemData["isSelected"]:
        reachableNodeIdDict.pop(nodeIndex[0])
    if upperTotemData["multiNode"]:
        for ranges in upperTotemData["selector"]:
            match ranges["range"]:
                case "ALL":
                    selectedNodeDict.update( {x:y for x,y in reachableNodeIdDict.items() if y["realNodeType"] in ranges["type"]})
                case "RIGHT":
                    selectedNodeDict.update({x:y for x,y in reachableNodeIdDict.items() if (y["realNodeType"] in ranges["type"]) and y["pos"]["x"] == ((currentPos["x"] if currentPos else -1) + 1)})
                case "CONNECTED":
                    selectedNodeDict.update(
                        {x:y \
                         for x,y in reachableNodeIdDict.items() \
                         if (y["realNodeType"] in ranges["type"]) \
                         and \
                         (\
                             [m for m in y["next"] \
                              if (not m["key"]) \
                              and \
                              (positionToIndex(m) == nodeIndex[0])\
                            ] \
                        or (positionToIndex(y["pos"]) in [positionToIndex(k) for k in [tmp for tmp in rlv2Data["current"]["map"]["zones"][zone]["nodes"][nodeIndex[0]]["next"] if not tmp["key"]]])\
                        )\
                        }
                    )
                    
                case "UP_AND_DOWN":
                    selectedNodeDict.update(
                        {x:y for x,y in reachableNodeIdDict.items() if (y["realNodeType"] in ranges["type"]) and [m for m in y["next"] if m["key"]]}
                    )
            
            selectedNodePos = sample(list(selectedNodeDict.keys()), len(selectedNodeDict) if ranges["amount"] > len(selectedNodeDict) else ranges["amount"])
    if upperTotemData["isSelected"]:
        selectedNodeDict.update(
            {
                nodeIndex[0]: rlv2Data["current"]["map"]["zones"][zone]["nodes"][nodeIndex[0]]
            }
        )
        selectedNodePos.append(str(nodeIndex[0]))
                    
    
    #下板：生效效果
    attachBuff = []
    rewards = []
    changeNode = None
    if lowerTotemData["basicEffect"]["attachBuff"]:
        attachBuff.append(
            lowerTotemData["basicEffect"]["buff"]
        )
    if lowerTotemData["basicEffect"]["immediateReward"]:
        rewards+=lowerTotemData["basicEffect"]["reward"]
    changeNode = lowerTotemData["basicEffect"]["nodeType"] if lowerTotemData["basicEffect"]["changeNode"] else None
    
    if extraEffect:
        if not lowerTotemData["extraEffect"]["coverBasicEffect"]:
            if lowerTotemData["extraEffect"]["attachBuff"]: 
                attachBuff.append(lowerTotemData["extraEffect"]["buff"])
            if lowerTotemData["extraEffect"]["immediateReward"]:
                rewards+=lowerTotemData["extraEffect"]["reward"]
            if lowerTotemData["extraEffect"]["changeNode"]:
                changeNode = lowerTotemData["extraEffect"]["nodeType"]
        else:
            if lowerTotemData["extraEffect"]["attachBuff"]: 
                attachBuff=[lowerTotemData["extraEffect"]["buff"]]
            if lowerTotemData["extraEffect"]["immediateReward"]:
                rewards=lowerTotemData["extraEffect"]["reward"]
            if lowerTotemData["extraEffect"]["changeNode"]:
                changeNode = lowerTotemData["extraEffect"]["nodeType"]
    genBattle = False
    for nodePos in selectedNodePos:
        if changeNode and not (rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["realNodeType"] in [4,32768,65536]) :
            rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["type"] = changeNode
            rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["realNodeType"] = changeNode
            rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["visibility"] = 0
            if changeNode == NodeType.ELITE_BATTLE:
                genBattle = True
            rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["alwaysVisible"] = True
        if attachBuff:
            rlv2Data["current"]["map"]["zones"][zone]["nodes"][str(nodePos)]["attach"] += attachBuff
    if genBattle:
        battleGenerator(rlv2Data["current"]["map"]["zones"], int(zone), [], None, True, selectedNodePos)
    if rewards:
        for item in rewards:
            gainItem(
                rlv2Data, 
                item["item"], 
                (len(selectedNodePos)*item["amount"] if item["countByNodeAmount"] else item["amount"]),
                item["item"],
                userSyncData,
                rlv2ExtensionData
            )
            
    #totemList[int(totemIndex[0][2])-1]["used"] = True
    #totemList[int(totemIndex[1][2])-1]["used"] = True
    clearExtraResponseData(rlv2Data, rlv2ExtensionData)
    rogueClass.rlv2 = rlv2Data
    rogueClass.extension = rlv2ExtensionData