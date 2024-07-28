from random import shuffle, random, choice
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_MODULE_DATA_PATH, ROGUE_RELIC_POOL_PATH
from server.core.utils.json import read_json
from .totemAndChaos import *

from ... import common
from ...common import NodeType
from math import floor
from random import randint


from ...common.rlv2tools import *
from .visionProcessor import *

roguePoolTable = read_json(ROGUE_RELIC_POOL_PATH)
rogueModuleTable = read_json(ROGUE_MODULE_DATA_PATH)
rogueTable = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
chaosPool = rogueModuleTable["rogue_3"]["chaos"]



def battleGenerator(mapData: dict, zone: int, pool: list, currentPosition: dict | None, fullyRandom: bool, randomNodePosIndexList) -> dict:
    if fullyRandom:
        for pos in randomNodePosIndexList:
            node = mapData[str(zone)]["nodes"][str(pos)]
            if node["realNodeType"] == NodeType.NORMAL_BATTLE:
                tmpPool = battlePoolGenerator(zone, "rogue_3")
                node["type"] = NodeType.NORMAL_BATTLE
                node["stage"] = choice(tmpPool)
            elif node["realNodeType"] == NodeType.ELITE_BATTLE:
                tmpPool = battlePoolGenerator(zone, "rogue_3")
                node["type"] = NodeType.ELITE_BATTLE
                node["stage"] = choice(tmpPool).replace("ro3_n_", "ro3_e_")
        return mapData
    else:
        return common.battleGenerator(mapData, zone, pool, currentPosition)

def eventGenerator(zone: int, pool: dict, theme: str) -> str:
    return common.eventGenerator(zone, pool, theme)


def battlePoolGenerator(zone: int, theme: str) -> list:
    return common.battlePoolGenerator(zone, theme)
        

def eventPoolGenerator(zone: int, currentPool: list, theme: str) -> list:
    return common.eventPoolGenerator(zone, currentPool, theme)

def getBattleBuffs(rogueData: dict, rogueExtension: dict):
    buffs = [
        {
            "key": "level_char_limit_add",
            "blackboard": [
                {
                    "key": "value",
                    "value": rogueExtension["extra_char_limit"],
                    "valueStr": None
                }
            ]
        },
        {
            "key": "char_attribute_mul",
            "blackboard": [
                {
                    "key": "atk",
                    "value": rogueExtension["extra_atk"] 
                }
            ]
        },
        {
            "key": "char_attribute_mul",
            "blackboard": [
                {
                    "key": "def",
                    "value": rogueExtension["extra_def"]
                }
            ]
        },
        {
            "key": "char_attribute_mul",
            "blackboard": [
                {
                    "key": "max_hp",
                    "value": rogueExtension["extra_hp"]
                }
            ]
        }
    ]
    currentNode = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]
    if currentNode["attach"]:
        for buff in currentNode["attach"]:
            buffs += rogueTable["details"][getTheme(rogueData)]["relics"][buff]["buffs"]
    if rogueData["current"]["module"]["chaos"]["chaosList"]:
        for chaos in rogueData["current"]["module"]["chaos"]["chaosList"]:
            buffs += rogueModuleTable["rogue_3"]["chaos"]["normalChaos"][chaos]["buff"] if len(chaos.split("_")) == 4 else rogueModuleTable["rogue_3"]["chaos"]["deeperChaos"][chaos]["buff"]
        
    themeBuffs = [
            # 0
            ([], []),
            # 1
            ([], []),
            # 2
            ([], []),
            # 3
            ([], []),
            # 4
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                ], []
            ),
            # 5
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [4]
            ),
            # 6
            ([], []),
            # 7
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], []
            ),
            # 8
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], []
            ),
            # 9
            (
                [], []
            ),
            # 10
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
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
                                "value": 1.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [5]
            ),
            # 11
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [8]
            ),
            # 12
            ([], []),
            # 13
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.05
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_damage_resistance[inf]"
                            },
                            {
                                "key": "damage_resistance",
                                "value": 0.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [11]
            ),
            # 14
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
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
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
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
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.15
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
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
                                "value": 1.1
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [7, 10]
            ),
            # 15
            (
                [
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
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
                                "value": 1.2
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "NORMAL"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.35
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
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
                                "value": 1.2
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "ELITE"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_atk_down"
                            },
                            {
                                "key": "atk",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                    {
                        "key": "global_buff_normal",
                        "blackboard": [
                            {
                                "key": "key",
                                "valueStr": "enemy_def_down"
                            },
                            {
                                "key": "def",
                                "value": 1.25
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
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
                                "value": 1.2
                            },
                            {
                                "key": "selector.enemy_level_type",
                                "valueStr": "BOSS"
                            }
                        ]
                    },
                ], [14]
            )
        ]
    return [buffs, themeBuffs]
    
    
def generateBattlePending(rogueData: dict, rogueExtension: dict, isEventBattle = False) -> dict:
    if isEventBattle:
        return {
            "index":getNextPendingIndex(rogueData),
            "type":"BATTLE",
            "content":{
                "battle":{
                    "state":0,
                    "addExcludeList":[]
                }
            }
        }
    boxInfo = {}
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
                boxInfo["trap_108_smbox"] = 1
    buffs = getBattleBuffs(rogueData, rogueExtension)
    return common.generateBattlePending(rogueData, rogueExtension, boxInfo, buffs[0], buffs[1])

def shopDiscount(rogueData: dict, rogueExtension: dict, goods: list):
    currentNode = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]
    currentNodeType = currentNode["type"]
    normalGoodsDiscount = 1
    rareGoodsDiscount = 1
    superRareGoodsDiscount = 1
    baseMultiplier = 1
    modifiedPrice = False
    
    if currentNode["attach"]:
        for buff in currentNode["attach"]:
            for nodeBuff in rogueTable["details"][getTheme(rogueData)]["relics"][buff]["buffs"]:
                if nodeBuff["key"] == "shop_discount_rarity" and currentNodeType == NodeType.SHOP:
                    modifiedPrice = True
                    match nodeBuff["blackboard"][2]["valueStr"]:
                        case "NORMAL":
                            normalGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])
                        case "RARE":
                            rareGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])
                        case "SUPER_RARE":
                            superRareGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])
                            
    chaosList = getChaos(rogueData)
    chaosBuff = []
    if chaosList:
        for chaos in chaosList:
            if len(chaos.split("_")) == 4:
                chaosBuff += chaosPool["normalChaos"][chaos]["buff"]
            if len(chaos.split("_")) == 5:
                chaosBuff += chaosPool["deeperChaos"][chaos]["buff"]
        for nodeBuff in chaosBuff:
            if nodeBuff["key"] == "shop_discount_rarity" and currentNodeType == NodeType.SHOP:
                modifiedPrice = True
                match nodeBuff["blackboard"][2]["valueStr"]:
                    case "NORMAL":
                        normalGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])
                    case "RARE":
                        rareGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])
                    case "SUPER_RARE":
                        superRareGoodsDiscount *= (1 + nodeBuff["blackboard"][1]["value"])    
    if isRelicExist(rogueData, "rogue_3_relic_legacy_58", rogueExtension):#锈蚀的铁锤
        baseMultiplier = 0.5
    for good in goods:
        if good["origCost"] <= 8:
            good["origCost"] *= baseMultiplier
            if normalGoodsDiscount != 1 or modifiedPrice:
                good["displayPriceChg"] = True
            good["priceCount"] = floor((good["origCost"] * normalGoodsDiscount) + 0.99)
            good["origCost"] = floor(good["origCost"] + 0.99)
        elif good["origCost"] <= 12:
            good["origCost"] *= baseMultiplier
            if rareGoodsDiscount != 1 or modifiedPrice:
                good["displayPriceChg"] = True
            good["priceCount"] = floor((good["origCost"] * rareGoodsDiscount) + 0.99)
            good["origCost"] = floor(good["origCost"] + 0.99)
        else:
            good["origCost"] *= baseMultiplier
            if superRareGoodsDiscount != 1 or modifiedPrice:
                good["displayPriceChg"] = True
            good["priceCount"] = floor((good["origCost"] * superRareGoodsDiscount) + 0.99)
            good["origCost"] = floor(good["origCost"] + 0.99)

def generateNonBattlePending(rogueData: dict, rogueExtension: dict, selectedChoices: str | None, userSyncData) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    currentNode = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]
    currentNodeType = currentNode["type"]
    
    if currentNode["attach"] and (not selectedChoices):
        for buff in currentNode["attach"]:
            for nodeBuff in rogueTable["details"][getTheme(rogueData)]["relics"][buff]["buffs"]:
                if nodeBuff["key"] == "totem_effect_reward":
                    gainItem(rogueData, nodeBuff["blackboard"][0]["valueStr"], nodeBuff["blackboard"][1]["value"], nodeBuff["blackboard"][0]["valueStr"], {}, rogueExtension=rogueExtension)

    if isRelicExist(rogueData, "rogue_3_relic_res_11", rogueExtension) and getVision(rogueData) >= 4:
        addGold(rogueData, 2)
                    
    match currentNodeType:
        case NodeType.SHOP:
            zone = getCurrentZone(rogueData)
            if zone == 1:
                shopId = "zone_1_shop"
            else:
                shopId = "zone_6_shop"
            goods = generateShopGoods(shopId, rogueData, rogueExtension)
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
                        "goods":goods,
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
            
        case NodeType.LOST_AND_FOUND:
            if isRelicExist(rogueData, "rogue_3_relic_explore_1", rogueExtension):
                addShield(rogueData, 2)
            pending = common.generateNonBattlePending(pendingIndex, currentNodeType, rogueData, rogueExtension)
        case NodeType.PASSAGE:
            if isRelicExist(rogueData, "rogue_3_relic_explore_1", rogueExtension):
                addShield(rogueData, 2)
            pending = common.generateNonBattlePending(pendingIndex, currentNodeType, rogueData, rogueExtension)
        case _:
            pending = common.generateNonBattlePending(pendingIndex, currentNodeType, rogueData, rogueExtension)
    return pending

def generateShopGoods(shopId: str, rogueData: dict, rogueExtension: dict):
    shopItemCount = 4
    goods = []
    theme = getTheme(rogueData)
    if rogueExtension["extraGoods1"]:
        shopItemCount += 1
    if rogueExtension["extraGoods2"]:
        shopItemCount += 1
    if rogueExtension["more_goods"]:
        shopItemCount += 2
    match shopId:
        case "zone_1_shop":
            index = 0
            if random() < 0.2:
                goods.append(
                    {
                        "index": f"{index}",
                        "itemId": choice([
                            x for x in [
                                f"{theme}_active_tool_1",
                                f"{theme}_active_tool_2",
                                f"{theme}_active_tool_3",
                                f"{theme}_active_tool_4",
                                f"{theme}_active_tool_5",
                                f"{theme}_active_tool_6"
                            ] if not isRelicExist(rogueData, x, rogueExtension)
                        ]),
                        "count": 1,
                        "priceId": f"{theme}_gold",
                        "priceCount": 8,    #折后价
                        "origCost": 8,
                        "displayPriceChg": False,
                        "_retainDiscount": 1
                    }
                )
                index += 1
                shopItemCount -= 1
            #招募券
            goods.append(
                {
                    "index": f"{index}",
                    "itemId": choice([
                        f"{theme}_recruit_ticket_medic",
                        f"{theme}_recruit_ticket_caster",
                        f"{theme}_recruit_ticket_pioneer"
                    ]),
                    "count": 1,
                    "priceId": f"{theme}_gold",
                    "priceCount": 4,    #折后价
                    "origCost": 4,
                    "displayPriceChg": False,
                    "_retainDiscount": 1
                }
            )
            index += 1
            shopItemCount -= 1
            pool = [x for x in roguePoolTable[theme]["shopRelicPool"] if not isRelicExist(rogueData, x, rogueExtension)]
            shuffle(pool)
            #藏品
            rareCount = 0
            superRareCount = 0
            valid = False
            for i in range(shopItemCount):
                relic = ""
                relicValue = 0 
                while not valid:
                    relic = relicLevelCheck(pool.pop(0), rogueExtension)
                    relicValue = rogueTable["details"][theme]["items"][relic]["value"]
                    match relicValue:
                        case 12:
                            if not rareCount >= 2:
                                rareCount += 1
                                valid = True
                        case 16:
                            if not superRareCount >= 1:
                                superRareCount += 1
                                valid = True
                        case _:
                            valid = True
                          
                goods.append(
                    {
                        "index": f"{index}",
                        "itemId": relic,
                        "count": 1,
                        "priceId": f"{theme}_gold",
                        "priceCount": relicValue,    #折后价
                        "origCost": relicValue,
                        "displayPriceChg": False,
                        "_retainDiscount": 1
                    }
                )
                valid = False
                index += 1
        case "zone_6_shop":
            index = 0
            goods.append(
                {
                    "index": f"{index}",
                    "itemId": "rogue_3_vision_item",
                    "count": 1,
                    "priceId": f"{theme}_gold",
                    "priceCount": 12,    #折后价
                    "origCost": 12,
                    "displayPriceChg": False,
                    "_retainDiscount": 1
                }
            )
            
            index += 1
            randomTotemId = choice(roguePoolTable["rogue_3"]["totemAll"])
            goods.append(
                {
                    "index": f"{index}",
                    "itemId": randomTotemId,
                    "count": 1,
                    "priceId": f"{theme}_gold",
                    "priceCount": rogueTable["details"]["rogue_3"]["items"][randomTotemId]["value"],    #折后价
                    "origCost": rogueTable["details"]["rogue_3"]["items"][randomTotemId]["value"],
                    "displayPriceChg": False,
                    "_retainDiscount": 1
                }
            )
            index += 1
            if random() < 0.2:
                goods.append(
                    {
                        "index": f"{index}",
                        "itemId": choice([
                            x for x in [
                                f"{theme}_active_tool_1",
                                f"{theme}_active_tool_2",
                                f"{theme}_active_tool_3",
                                f"{theme}_active_tool_4",
                                f"{theme}_active_tool_5",
                                f"{theme}_active_tool_6"
                            ] if not isRelicExist(rogueData, x, rogueExtension)
                        ]),
                        "count": 1,
                        "priceId": f"{theme}_gold",
                        "priceCount": 8,    #折后价
                        "origCost": 8,
                        "displayPriceChg": False,
                        "_retainDiscount": 1
                    }
                )
                index += 1
                shopItemCount -= 1
            #招募券
            recruitTicketPool = [
                "rogue_3_recruit_ticket_special",
                "rogue_3_recruit_ticket_warrior",
                "rogue_3_recruit_ticket_tank",
                "rogue_3_recruit_ticket_support",
                "rogue_3_recruit_ticket_sniper",
                "rogue_3_recruit_ticket_medic",
                "rogue_3_recruit_ticket_pioneer",
                "rogue_3_recruit_ticket_caster",
            ] * 6 + [
                "rogue_3_recruit_ticket_double_1",
                "rogue_3_recruit_ticket_double_2",
                "rogue_3_recruit_ticket_double_3",
                "rogue_3_recruit_ticket_double_4",
            ] * 3 + [
                "rogue_3_recruit_ticket_quad_melee",
                "rogue_3_recruit_ticket_quad_ranged"
            ]
            
            for i in range(2):
                shuffle(recruitTicketPool)
                ticket = recruitTicketPool.pop()
                recruitTicketPool = [x for x in recruitTicketPool if x != ticket]
                goods.append(
                    {
                        "index": f"{index}",
                        "itemId": ticket,
                        "count": 1,
                        "priceId": f"{theme}_gold",
                        "priceCount": 5 if len(ticket.split("_")) > 5 else 4,    #折后价
                        "origCost": 5 if len(ticket.split("_")) > 5 else 4,
                        "displayPriceChg": False,
                        "_retainDiscount": 1
                    }
                )
                index += 1
                shopItemCount -= 1
            
            
            pool = [x for x in roguePoolTable[theme]["shopRelicPool"] if not isRelicExist(rogueData, x, rogueExtension)]
            shuffle(pool)
            #藏品
            rareCount = 0
            superRareCount = 0
            valid = False
            for i in range(shopItemCount):
                relic = ""
                relicValue = 0 
                while not valid:
                    relic = relicLevelCheck(pool.pop(0), rogueExtension)
                    relicValue = rogueTable["details"][theme]["items"][relic]["value"]
                    match relicValue:
                        case 12:
                            if not rareCount >= 2:
                                rareCount += 1
                                valid = True
                        case 16:
                            if not superRareCount >= 1:
                                superRareCount += 1
                                valid = True
                        case _:
                            valid = True
                                
                goods.append(
                    {
                        "index": f"{index}",
                        "itemId": relic,
                        "count": 1,
                        "priceId": f"{theme}_gold",
                        "priceCount": relicValue,    #折后价
                        "origCost": relicValue,
                        "displayPriceChg": False,
                        "_retainDiscount": 1
                    }
                )
                valid = False
                index += 1
    shopDiscount(rogueData, rogueExtension, goods)
    return goods
    

def generateBattleRewardPending(rogueData: dict, rogueExtension: dict, stageName: str, stageType: int, decryptedBattleData: dict, gainExp = 0, gainGold = 0) -> dict:
    battleStats = decryptedBattleData["battleData"]["stats"]["charStats"]
    theme = getTheme(rogueData)
    if stageType == NodeType.ELITE_BATTLE:
        isElite = True
        isBoss = False
    elif stageType == NodeType.BOSS:
        isElite = False
        isBoss = True
    else:
        isElite = False
        isBoss = False
    normalBoxCount = 0
    rareBoxCount = 0
    superRareBoxCount = 0
    ticketCount = 0
    if getCurrentZone(rogueData) in [1,3,5]:
        ticketCount = 1
    elif getCurrentZone(rogueData) in [2,4,6]:
        ticketCount = 2
    else:
        pass
        #TODO:罗德岛战术电台
    for item in battleStats:
        if item["Key"]["charId"] == "trap_108_smbox" and item["Key"]["counterType"] == "DEAD":
            normalBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_109_smrbox" and item["Key"]["counterType"] == "DEAD":
            rareBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_110_smbbox" and item["Key"]["counterType"] == "DEAD":
            superRareBoxCount += item["Value"]

    return common.generateBattleRewardPending(
        rogueData, 
        rogueExtension, 
        stageName, 
        stageType,
        decryptedBattleData,
        theme,
        generateBattleRewards(stageName, isElite, isBoss, gainGold, {"normalBox": normalBoxCount, "rareBox": rareBoxCount, "superRareBox": superRareBoxCount}, theme, ticketCount, rogueExtension, rogueData["current"]["inventory"]["relic"], rogueData),
        gainExp
    )



def generateBattleRewards(stage: str, isElite: bool, isBoss: bool, gainGold: int, chestInfo: dict, theme: str, ticketCount = 1, rogueExtension: dict = {}, hasRelicInfo: dict = {}, rogueData = {}) -> list:
    index = 0
    rewards = []
    #TODO:根据是否在树洞更改部分资源掉落概率
    baseRewards = common.generateBaseBattleRewards(
        stage,
        isElite,
        isBoss,
        gainGold,
        chestInfo,
        theme,
        {
            "relicChance":{
                "isElite": 1.0,
                "notElite": 0.05
            }
        },
        ticketCount, 
        rogueExtension,
        hasRelicInfo,
        rogueData,
        1 if isRelicExist(rogueData, "rogue_3_relic_legacy_60",rogueExtension) else 0,
        2 if isRelicExist(rogueData, "rogue_3_relic_legacy_59", rogueExtension, 2) else (1 if isRelicExist(rogueData, "rogue_3_relic_legacy_59",rogueExtension) else 0),
    )
    rewards = baseRewards["rewards"]
    index = baseRewards["lastIndex"]
    relicPool = baseRewards["relicPool"]
    lifeChance = 0.5
    visionChance = 0.12
    totemChance = 1 if isBoss else (0.8 if isElite else 0.4)
    
    
    #TODO 掉落顺序4：生命值
    if random() < lifeChance:
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_hp",
                        "count":1
                    }
                ],
                "done": 0
                }
            )
        index += 1
    if getHp(rogueData) <= rogueExtension["add_hp_limit_hp"]:
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_hp",
                        "count":1
                    }
                ],
                "done": 0
                }
            )
        index += 1
    if isRelicExist(rogueData, "rogue_3_relic_legacy_62", rogueExtension):
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_hp",
                        "count":1
                    }
                ],
                "done": 0
                }
            )
        index += 1
    #TODO 掉落顺序5：抗干扰指数
    if random() < visionChance:
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": f"{theme}_vision",
                        "count":1
                    }
                ],
                "done": 0
                }
            )
        index += 1
    #TODO 掉落顺序6：密文版
    #TODO 修辞
    if random() < totemChance:
        totemAmount = (2 if isBoss else 1) + (1 if rogueExtension["more_totem"] else 0)
        if isRelicExist(rogueData, "rogue_3_relic_explore_5", rogueExtension) and random() < 0.15:
            extraTotem = True
        else:
            extraTotem = False
        totemItems = []
        totemPool = roguePoolTable[f"{theme}"]["totemAll"]
        
        for i in range(totemAmount):
            shuffle(totemPool)
            totemItems.append(
                {
                    "sub": i,
                    "id": totemPool.pop(),
                    "count": 10
                }
            )
        rewards.append(
            {
                "index": index,
                "items":totemItems,
                "done": 0
                }
            )
        index += 1
        if extraTotem:
            rewards.append(
                {
                    "index": index,
                    "items":choice(totemPool),
                    "done": 0
                }
            )
            index += 1
        
    #掉落顺序7：密文版馈赠
    currentNode = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]
    if currentNode["attach"]:
        for buff in currentNode["attach"]:
            for nodeBuff in rogueTable["details"][getTheme(rogueData)]["relics"][buff]["buffs"]:
                if nodeBuff["key"] == "totem_effect_reward":
                    if nodeBuff["blackboard"][0]["valueStr"] != "pool_battle_only":
                        rewards.append(
                        {
                            "index": index,
                            "items":[
                                {
                                    "sub": 0,
                                    "id": nodeBuff["blackboard"][0]["valueStr"],
                                    "count":nodeBuff["blackboard"][1]["value"]
                                }
                            ],
                            "done": 0,
                            "exDropSrc": "TOTEM_EXTRA"
                            }
                        )
                        index += 1
                    else:
                        hasRelicInfo = rogueData["current"]["inventory"]["relic"]
                        hasRelic = [x["id"] for x in hasRelicInfo.values()]
                        relics = [i for i in roguePoolTable[theme]["battleRelicPool"] if not (i in hasRelic)]
                        relic = relicLevelCheck(relics.pop(randint(0,len(relics) - 1)),rogueExtension)
                        rewards.append(
                            {
                                "index": index,
                                "items":[
                                    {
                                        "sub": 0,
                                        "id": relic,
                                        "count":1
                                    }
                                ],
                                "done": 0,
                                "exDropSrc": "TOTEM_EXTRA"
                                }
                            )
                        index += 1
    return rewards
        

def gainItemsAfterBattle(rogueData: dict, index: int, subIndex: int, userData = None, rogueExtension = None):
    common.gainItemsAfterBattle(rogueData, index, subIndex, userData, rogueExtension, gainItem)
    

def gainItem(rogueData: dict, itemType: str, amount: int, item: str, userSyncData, rogueExtension):
    if not itemType:
        itemType = item
    match itemType:        
        case itemType if itemType.find("totem") != -1:
            addTotem(rogueData, itemType)
        case itemType if itemType.find("vision") != -1:
            addVision(rogueData, amount, rogueExtension)
        case "rogue_3_vision_item":
            addVision(rogueData, 1, rogueExtension)
        case "rogue_3_chaos_purify":
            increaseChaosValue(rogueData, rogueExtension, -amount)
            if rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]["type"] == NodeType.SHOP:
                shopDiscount(rogueData, rogueExtension, rogueData["current"]["player"]["pending"][0]["content"]["battleShop"]["goods"])
        case itemType if itemType.find("chaos") != -1:
            increaseChaosValue(rogueData, rogueExtension, amount)
            if rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]["type"] == NodeType.SHOP:
                shopDiscount(rogueData, rogueExtension, rogueData["current"]["player"]["pending"][0]["content"]["battleShop"]["goods"])
        case "pool_battle_only":
            hasRelicInfo = rogueData["current"]["inventory"]["relic"]
            hasRelic = [x["id"] for x in hasRelicInfo.values()]
            relics = [i for i in roguePoolTable[getTheme(rogueData)]["battleRelicPool"] if not (i in hasRelic)]
            relic = relicLevelCheck(relics.pop(randint(0,len(relics) - 1)), rogueExtension)
            addRelic(rogueData, relic)
        case _:
            common.gainItem(rogueData, itemType, amount, item, userSyncData, rogueExtension, customProcessRelic=processRelic)
        
           
def activateTickets(rogueData: dict, item, userSyncData, rogueExtension, ticketId):
    common.activateTickets(rogueData, item, userSyncData, rogueExtension, ticketId)
    
def processRelic(rogueData, rogueExtension, index, userSyncData):
    relicId = rogueData["current"]["inventory"]["relic"][index]["id"]
    relicDetail = rogueTable["details"]["rogue_3"]["relics"][relicId]
    common.processRelic(rogueData, rogueExtension, index, userSyncData, gainItem)
    if relicId.find("rogue_3_relic_legacy_54") != -1:           #TODO:2为直升，但是现在还没做
        rogueExtension["upgrade_bonus_4"] = 1
    if relicId.find("rogue_3_relic_legacy_55") != -1:
        rogueExtension["upgrade_bonus_5"] = 1
    if relicId.find("rogue_3_relic_legacy_56") != -1:
        rogueExtension["upgrade_bonus_6"] = 1
    if relicId.find("rogue_3_relic_legacy_57") != -1:
        rogueExtension["recruit_discount_all"] = True
    
    if relicId.find("rogue_3_relic_legacy_58") != -1 and rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]["type"] == NodeType.SHOP:
        shopDiscount(rogueData, rogueExtension, rogueData["current"]["player"]["pending"][0]["content"]["battleShop"]["goods"])
        
    if relicId.find("rogue_3_relic_legacy_163") != -1:
        addShield(rogueData, getHp(rogueData))
        addHp(rogueData, -99999)
    if relicId.find("rogue_3_relic_fight_14") != -1:
        hasRelicInfo = rogueData["current"]["inventory"]["relic"]
        hasRelic = [x["id"] for x in hasRelicInfo.values()]
        relics = [i for i in roguePoolTable["rogue_3"]["cheapStuffPool"] if not (i in hasRelic)]
        items = []
        itemsId = []
        for i in range(3):
            shuffle(relics)
            relic = relicLevelCheck(relics.pop(), rogueExtension)
            gainItem(rogueData, relic, 1, relic, userSyncData, rogueExtension)
            items.append(
                {
                    "id": relic,
                    "count": 1
                }
            )
            itemsId.append(relic)
        writeExtraResponseData(
            rogueData, 
            rogueExtension, 
            {
                "items": items,
                "pushMessage":[
                    {
                        "path":"rlv2GotRandRelic",
                        "payload":{
                            "idList":itemsId
                        }
                    }
                ]
            }
        )
        
        
    
            
    
def relicLevelCheck(relicId: str, rogueExtension: dict):
    return common.relicLevelCheck(relicId, rogueExtension)
    
def generateTickets(ticketBaseObject: dict, upgradeChance: float):
    common.generateTickets(ticketBaseObject, upgradeChance, "rogue_3")
    
    
