from server.core.utils.json import read_json

from ...common import NodeType
from server.constants import ROGUE_RELIC_POOL_PATH, ROGUE_MODULE_DATA_PATH


from ...common.rlv2tools import *

totemPool = read_json(ROGUE_RELIC_POOL_PATH)["rogue_3"]["totemAll"]
chaosPool = read_json(ROGUE_MODULE_DATA_PATH)["rogue_3"]["chaos"]


def getVision(rlv2_data: dict):
    return rlv2_data["current"]["module"]["vision"]["value"]

def setVision(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["vision"]["value"] = sets
    
def addVision(rlv2_data: dict, add: int, rogueExtension: dict):   #ROGUE_3独有
    rlv2_data["current"]["module"]["vision"]["value"] += add
    if add < 0 and isRelicExist(rlv2_data, "rogue_3_relic_res_9", rogueExtension):
        addHp(rlv2_data, 1)
    visionChecker(rlv2_data, rogueExtension)
    visionGenerator(getCurrentZone(rlv2_data), getPosition(rlv2_data), getVision(rlv2_data), rlv2_data["current"]["map"]["zones"])
    
def visionChecker(rogueData: dict, rogueExtension: dict):
    currentVision = getVision(rogueData)
    if currentVision > 6:          #琥珀伤痕
        existence = isRelicExist(rogueData, "rogue_3_relic_res_12", rogueExtension)
        if existence:
            setRelicLayer(rogueData, existence[1], currentVision - 6)
        else:
            setVision(rogueData, 6)
        rogueData["current"]["module"]["vision"]["isMax"] = True
    if currentVision < 6 and (rogueData["current"]["module"]["vision"]["isMax"]):
        rogueData["current"]["module"]["vision"]["isMax"] = False
    if currentVision < 0:
        setVision(rogueData, 0)
        
        
def visionGenerator(zone: int, currentPosition: dict | None, vision: int, mapData: dict) -> dict:
    return generateSightByVision(zone, currentPosition, vision, mapData)


def generateSightByVision(zone: int, currentPosition: dict | None, vision: int, mapData: dict) -> dict:
    if not currentPosition:
        position = {
            "x": -1,
            "y": 0
        }
    else:
        position = currentPosition
        
    currentNode = mapData[str(zone)]["nodes"][positionToIndex(position)]
    nextNode = [mapData[str(zone)]["nodes"][positionToIndex(node)] \
            for node in currentNode["next"]]  if position["x"] != -1 else [mapData[str(zone)]["nodes"][str(node["pos"]["y"])] \
            for node in mapData[str(zone)]["nodes"].values() if node["pos"]["x"] == 0]
    
    match vision:
        case 0:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
                    continue
                if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                    #node["realNodeType"] = node["type"]
                    node["type"] = NodeType.UNKNOWN
                    node["visibility"] = 2
                elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                    #node["realNodeType"] = node["type"]
                    node["type"] = NodeType.UNKNOWN
                    node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 1 | 2:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
                    continue
                if node["pos"]["x"] > position["x"] + 1:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 3:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
                    continue
                if node["pos"]["x"] > position["x"] + 2:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 4 | 5:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
                    continue
                if node["pos"]["x"] > position["x"] + 3:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case vision if vision >= 6:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
                    continue
                if node["pos"]["x"] > position["x"] + 99999:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"]= NodeType.UNKNOWN
                        node["visibility"]= 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
                    
    for node in nextNode:
        node["type"] = node["realNodeType"]
    if currentNode:
        currentNode["visibility"] = 0
        currentNode["type"] = currentNode["realNodeType"]
    return mapData