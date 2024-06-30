from sqlalchemy.pool import Pool
from server.constants import ROGUE_RELIC_POOL_PATH, ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_ROUTE_PATH
from random import shuffle, randint, sample, random, choice
from server.core.utils.json import read_json

from server.core.utils.rogueHandler.rogue_3.tools.map import NodeType


from ..tools.rlv2tools import *

rogueTable: dict = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
roguePoolTable = read_json(ROGUE_RELIC_POOL_PATH)


ZONE_1_NORMAL_BATTLE_POOL = [
    "ro3_n_1_1",            #死囚之夜
    "ro3_n_1_2",            #度假村冤魂
    "ro3_n_1_3",            #苔手
    "ro3_n_1_4",            #待宰的兽群
    "ro3_n_1_5"             #事不过四（DLC2内容）
]
ZONE_2_NORMAL_BATTLE_POOL = [
    "ro3_n_2_1",            #没有尽头的路
    "ro3_n_2_2",            #低空机动
    "ro3_n_2_3",            #幽影与鬼魅
    "ro3_n_2_4",            #违和
    "ro3_n_2_5",            #虫虫别回头
    "ro3_n_2_6"             #还之彼身（DLC2内容）
]
ZONE_3_NORMAL_BATTLE_POOL = [
    "ro3_n_3_1",            #弄假成真
    "ro3_n_3_2",            #饥渴祭坛
    "ro3_n_3_3",            #狡兽九窟
    "ro3_n_3_4",            #冰海疑影
    "ro3_n_3_5",            #咫尺天涯
    "ro3_n_3_6",            #思维折断
    "ro3_n_3_7"             #恃强凌弱（DLC2内容）
]
ZONE_4_NORMAL_BATTLE_POOL = [
    "ro3_n_4_1",            #公司纠葛
    "ro3_n_4_2",            #应用测试
    "ro3_n_4_3",            #坍缩体的午后
    "ro3_n_4_4",            #大迁徙
    "ro3_n_4_5",            #以守代攻
    "ro3_n_4_6",            #杂音干扰
    "ro3_n_4_7",            #禁区
    "ro3_n_4_8"             #冰凝之所（DLC2内容）
]
ZONE_5_NORMAL_BATTLE_POOL = [
    "ro3_n_5_1",            #乐理之灾
    "ro3_n_5_2",            #生人勿近
    "ro3_n_5_3",            #混乱的表象
    "ro3_n_5_4",            #求敌得敌
    "ro3_n_5_5",            #亡者行军
    "ro3_n_5_6",            #何处无山海
    "ro3_n_5_7",            #本能污染
    "ro3_n_5_8"             #人造物狂欢节（DLC2内容）
]
ZONE_6_NORMAL_BATTLE_POOL = [
    "ro3_n_6_1",            #霜与沙
    "ro3_n_6_2"             #生灵的终点
]


ZONE_1_EMERGENCY_BATTLE_POOL = [
    "ro3_e_1_1",            #死囚之夜
    "ro3_e_1_2",            #度假村冤魂
    "ro3_e_1_3",            #苔手
    "ro3_e_1_4",            #待宰的兽群
    "ro3_e_1_5"             #事不过四（DLC2内容）
]
ZONE_2_EMERGENCY_BATTLE_POOL = [
    "ro3_e_2_1",            #没有尽头的路
    "ro3_e_2_2",            #低空机动
    "ro3_e_2_3",            #幽影与鬼魅
    "ro3_e_2_4",            #违和
    "ro3_e_2_5",            #虫虫别回头
    "ro3_e_2_6"             #还之彼身（DLC2内容）
]
ZONE_3_EMERGENCY_BATTLE_POOL = [
    "ro3_e_3_1",            #弄假成真
    "ro3_e_3_2",            #饥渴祭坛
    "ro3_e_3_3",            #狡兽九窟
    "ro3_e_3_4",            #冰海疑影
    "ro3_e_3_5",            #咫尺天涯
    "ro3_e_3_6",            #思维折断
    "ro3_e_3_7"             #恃强凌弱（DLC2内容）
]
ZONE_4_EMERGENCY_BATTLE_POOL = [
    "ro3_e_4_1",            #公司纠葛
    "ro3_e_4_2",            #应用测试
    "ro3_e_4_3",            #坍缩体的午后
    "ro3_e_4_4",            #大迁徙
    "ro3_e_4_5",            #以守代攻
    "ro3_e_4_6",            #杂音干扰
    "ro3_e_4_7",            #禁区
    "ro3_e_4_8"             #冰凝之所（DLC2内容）
]
ZONE_5_EMERGENCY_BATTLE_POOL = [
    "ro3_e_5_1",            #乐理之灾
    "ro3_e_5_2",            #生人勿近
    "ro3_e_5_3",            #混乱的表象
    "ro3_e_5_4",            #求敌得敌
    "ro3_e_5_5",            #亡者行军
    "ro3_e_5_6",            #何处无山海
    "ro3_e_5_7",            #本能污染
    "ro3_e_5_8"             #人造物狂欢节（DLC2内容）
]
ZONE_6_EMERGENCY_BATTLE_POOL = [
    "ro3_e_6_1",            #霜与沙
    "ro3_e_6_2"             #生灵的终点
]





def battleGenerator(mapData: dict, zone: int, pool: list, currentPosition: dict | None) -> dict:
    if not currentPosition:
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
        currentNode = mapData[str(zone)]["nodes"][f"{currentPosition["x"]}0{currentPosition["y"]}" if currentPosition["x"] != 0 else f"{currentPosition["y"]}"]
        nextNode = [mapData[str(zone)]["nodes"][f"{node["x"]}0{node["y"]}"] \
            for node in currentNode["next"]]
        #print(nextNode)
        for node in nextNode:
            if not node["stage"]:
                #print(1)
                #print(node["realNodeType"], NodeType.NORMAL_BATTLE)
                #print(node["realNodeType"] == NodeType.NORMAL_BATTLE)
                #print(node["realNodeType"] == NodeType.ELITE_BATTLE)
                #print(int(node["realNodeType"]) == NodeType.ELITE_BATTLE)
                #print(int(node["realNodeType"]) == NodeType.NORMAL_BATTLE)
                if node["realNodeType"] == NodeType.NORMAL_BATTLE:
                    node["type"] = NodeType.NORMAL_BATTLE
                    if (currentNode["realNodeType"] == NodeType.NORMAL_BATTLE) or (currentNode["realNodeType"] == NodeType.ELITE_BATTLE):
                        pool.insert(0,pool.pop(pool.index(currentNode["stage"].replace("ro3_e_", "ro3_n_"))))
                    #print(pool)
                    node["stage"] = pool.pop()
                    #print(node["stage"])
                    #print(pool)
                    pool.insert(0, node["stage"])
                elif node["realNodeType"] == NodeType.ELITE_BATTLE:
                    node["type"] = NodeType.ELITE_BATTLE
                    if (currentNode["realNodeType"] == NodeType.NORMAL_BATTLE) or (currentNode["realNodeType"] == NodeType.ELITE_BATTLE):
                        pool.insert(0,pool.pop(pool.index(currentNode["stage"].replace("ro3_e_", "ro3_n_"))))
                    #print(pool)
                    node["stage"] = pool.pop().replace("ro3_n_", "ro3_e_")
                    #print(node["stage"])
                    #print(pool)
                    pool.insert(0, node["stage"].replace("ro3_e_", "ro3_n_"))
        shuffle(pool)
        return mapData

def eventGenerator(zone: int, pool: dict, mapData: dict) -> dict:
    pass


def battlePoolGenerator(zone: int) -> list:
    if zone == 114514:          ##测试
        zone = 4
    match zone:
        case 1:
            pool = ZONE_1_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 2:
            pool = ZONE_2_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 3:
            pool = ZONE_3_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 4:
            pool = ZONE_4_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 5:
            pool = ZONE_5_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 6:
            pool = ZONE_6_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        case 7:
            pool = ZONE_6_NORMAL_BATTLE_POOL
            shuffle(pool)
            return pool
        

def eventPoolGenerator(zone: int) -> dict:
    pass

def getBattleBuffs(rogueData: dict, rogueExtension: dict) -> dict:
    buffs = []
    
    buffs += [
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
    modeGrade = getModeGrade(rogueData)
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
    
    if modeGrade > 4:
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
        if item_id in rogueTable["details"]["rogue_3"]["relics"]:
            buffs += rogueTable["details"]["rogue_3"]["relics"][item_id]["buffs"]
        
    return buffs
    
    
def generateBattlePending(rogueData: dict, rogueExtension: dict) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    battleBuffs = getBattleBuffs(rogueData, rogueExtension)
    
    box_info = {}
    chestCnt = 0
    for i in range(2):
        rd = random()
        if rd <= 0.015:
            chestCnt += 1
            if box_info.__contains__("trap_110_smbbox"):
                box_info["trap_110_smbbox"] += 1
            else:
                box_info["trap_110_smbbox"] = 1
        elif rd <= 0.045:
            chestCnt += 1
            if box_info.__contains__("trap_109_smrbox"):
                box_info["trap_109_smrbox"] += 1
            else:
                box_info["trap_109_smrbox"] = 1
        elif rd <= 0.15:
            chestCnt += 1
            if box_info.__contains__("trap_108_smbox"):
                box_info["trap_108_smbox"] += 1
            else:
                box_info["trap_108_smbox"] = 1
    pending = {
        "index":pendingIndex,
        "type":"BATTLE",
        "content":{
            "battle":{
                "state":1,
                "chestCnt":0,
                "goldTrapCnt":0,
                "diceRoll":[],
                "boxInfo":box_info,
                "tmpChar":[],
                "sanity":0,
                "unKeepBuff":battleBuffs
            }
        }
    }
    
    return pending
    
def generateBattleRewardPending(rogueData: dict, rogueExtension: dict, stageName: str, stageType: int, decryptedBattleData: dict, gainExp = 0, gainGold = 0) -> dict:
    pendingIndex = getNextPendingIndex(rogueData)
    
    lastHp = decryptedBattleData["battleData"]["stats"]["leftHp"]
    battleStats = decryptedBattleData["battleData"]["stats"]["charStats"]
    
    normalBoxCount = 0
    rareBoxCount = 0
    superRareBoxCount = 0
    for item in battleStats:
        if item["Key"]["charId"] == "trap_108_smbox" and item["Key"]["counterType"] == "DEAD":
            normalBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_109_smrbox" and item["Key"]["counterType"] == "DEAD":
            rareBoxCount += item["Value"]
        elif item["Key"]["charId"] == "trap_110_smbbox" and item["Key"]["counterType"] == "DEAD":
            superRareBoxCount += item["Value"]
            
    chestInfo = {
        "normalBox": normalBoxCount,
        "rareBox": rareBoxCount,
        "superRareBox": superRareBoxCount
    }
    addInfo = addExp(rogueData, gainExp)
    if addInfo["hpLimit"]:
        lastHp += addInfo["hpLimit"]
    
    if lastHp <= getHp(rogueData):
        gainShield = -getShield(rogueData)
        damageHp = getHp(rogueData) - lastHp
    else:
        gainShield = -(getHp(rogueData) + getShield(rogueData) - lastHp)
        damageHp = 0
        
    if stageType == NodeType.ELITE_BATTLE:
        isElite = True
        isBoss = False
    elif stageType == NodeType.BOSS:
        isElite = False
        isBoss = True
    else:
        isElite = False
        isBoss = False
    
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
    if getCurrentZone(rogueData) in [1,3,5]:
        ticketCount = 1
    elif getCurrentZone(rogueData) in [2,4]:
        ticketCount = 2
    else:
        pass
        #TODO:罗德岛战术电台
    
    pending["content"]["battleReward"]["rewards"] = generateBattleRewards(stageName, isElite, isBoss, gainGold, chestInfo, ticketCount, rogueExtension, rogueData["current"]["inventory"]["relic"])
    pending["content"]["battleReward"]["show"] = randint(0, len(rogueData["current"]["troop"]["chars"]) - 1)
    addShield(rogueData, gainShield)
    addHp(rogueData, -damageHp)
    return pending



def generateBattleRewards(stage: str, isElite: bool, isBoss: bool, gainGold: int, chestInfo: dict, ticketCount = 1, rogueExtension: dict = {}, hasRelicInfo: dict = {}) -> list:
    index = 0
    rewards = []
    #TODO:根据是否在树洞更改部分资源掉落概率
    lifeChance = 0.05
    visionChance = 0.12
    totemChance = 0.8 if isElite else 0.4
    relicChance = 0.05 if isElite else 1.0
    #掉落顺序1：原石锭
    rewards.append(
        {
            "index": index,
            "items":[
                {
                    "sub": 0,
                    "id": "rogue_3_gold",
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
                        "id": "rogue_3_gold",
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
                        "id": "rogue_3_gold",
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
                        "id": "rogue_3_gold",
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
    if random() < relicChance:
        hasRelic = [x["id"] for x in hasRelicInfo.values()]
        relics = [i for i in roguePoolTable["rogue_3"]["battleRelicPool"] if not (i in hasRelic)]
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": relics.pop(randint(0,len(relics) - 1)),
                        "count":1
                    }
                ],
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
    
    generateTickets(ticketBaseObject, upgradeChance)
    rewards.append(ticketBaseObject)
    index += 1
    #TODO 掉落顺序4：生命值
    if random() < lifeChance:
        rewards.append(
            {
                "index": index,
                "items":[
                    {
                        "sub": 0,
                        "id": "rogue_3_hp",
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
                        "id": "rogue_3_vision",
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
        totemAmount = 2 if rogueExtension else 1
        totemItems = []
        totemPool = roguePoolTable["rogue_3"]["totemAll"]
        for i in range(totemAmount):
            shuffle(totemPool)
            totemItems.append(
                {
                    "sub": i,
                    "id": totemPool.pop(),
                    "count": 1
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
    return rewards
        

def gainItemsAfterBattle(rogueData: dict, index: int, subIndex: int):
    #TODO 招募券以及典训藏品的激活，部分加携带/生命值/护盾/希望等等的资源增加，部分藏品的特殊效果（密信系列的招募减希望/直升，和坍缩值/指挥经验相关机制，叠层藏品）
    battleRewardsPending = rogueData["current"]["player"]["pending"]
    itemType: str = battleRewardsPending[0]["content"]["battleReward"]["rewards"][index]["items"][subIndex]["id"]
    itemCount = battleRewardsPending[0]["content"]["battleReward"]["rewards"][index]["items"][subIndex]["count"]
    item = battleRewardsPending[0]["content"]["battleReward"]["rewards"][index]
    match itemType:
        case itemType if itemType.find("gold") != -1:
            gainItem(rogueData, "gold", itemCount)
            item["done"] = 1
        case itemType if itemType.find("recruit_ticket") != -1:
            gainItem(rogueData, "recruit_ticket", itemCount, itemType)
            item["done"] = 1
        case itemType if itemType.find("totem") != -1:
            gainItem(rogueData, "totem", itemCount, itemType)
            item["done"] = 1
        case itemType if itemType.find("vision") != -1:
            gainItem(rogueData, "vision", itemCount)
            item["done"] = 1
        case itemType if itemType.find("relic") != -1:
            gainItem(rogueData, "relic", itemCount, itemType)
            item["done"] = 1
        case itemType if itemType.find("shield") != -1:
            gainItem(rogueData, "shield", itemCount)
            item["done"] = 1
        case itemType if itemType.find("population") != -1:
            gainItem(rogueData, "population", itemCount)
            item["done"] = 1
        case itemType if itemType.find("explore_tool") != -1:     #深入调查
            gainItem(rogueData, "explore_tool", itemCount)
            item["done"] = 1
        case itemType if itemType.find("active_tool") != -1:        #支援装置       
            gainItem(rogueData, "active_tool", itemCount)
            item["done"] = 1
        case itemType if itemType.find("rogue_3_hp") != -1:              
            gainItem(rogueData, "hp", itemCount)
            item["done"] = 1
        
def gainItem(rogueData: dict, itemType: str, amount: int, item = None):
    match itemType:
        case "gold":
            addGold(rogueData, amount)
        case "recruit_ticket":
            #activeTicket(rogueData, item)
            pass
        case "totem":
            addTotem(rogueData, item)
        case "vision":
            addVision(rogueData, amount)
        case "relic":
            addRelic(rogueData, item)
        case "shield":
            addShield(rogueData, amount)
        case "population":
            addPopulation(rogueData, amount)
        case "hp":
            addHp(rogueData, amount)
        case "explore_tool":     #深入调查
            pass
        case "active_tool":        #支援装置       
            pass
            
    
def generateTickets(ticketBaseObject: dict, upgradeChance: float):
    ticketPool = [
        "rogue_3_recruit_ticket_pioneer",
        "rogue_3_recruit_ticket_warrior",
        "rogue_3_recruit_ticket_tank",
        "rogue_3_recruit_ticket_sniper",
        "rogue_3_recruit_ticket_caster",
        "rogue_3_recruit_ticket_support",
        "rogue_3_recruit_ticket_medic",
        "rogue_3_recruit_ticket_special"
    ]
    upgradePool: list = [
        "rogue_3_recruit_ticket_all_premium",
        "rogue_3_recruit_ticket_all_discount",
        "rogue_3_upgrade_ticket_all"
    ]
    pioneer_and_warrior_pool = [
        "rogue_3_recruit_ticket_quad_melee_discount",
        "rogue_3_recruit_ticket_double_1"
    ]
    tank_and_support_pool = [
        "rogue_3_recruit_ticket_double_2"
    ]
    sniper_and_medic_pool = [
        "rogue_3_recruit_ticket_quad_ranged_discount",
        "rogue_3_recruit_ticket_double_3"
    ]
    caster_and_special_pool = [
        "rogue_3_recruit_ticket_double_4"
    ]
    allProfession = True
    for item in ticketBaseObject["items"]:
        item["id"] = choice(ticketPool)
        ticketPool.pop(ticketPool.index(item["id"]))
        match item["id"][23:]:
            case "pioneer" | "warrior":
                if random() < upgradeChance and pioneer_and_warrior_pool:
                    item["id"] = pioneer_and_warrior_pool.pop()
                elif allProfession and random() < (upgradeChance * upgradeChance):
                    item["id"] = choice([upgradePool])
                    allProfession = False
            case "tank" | "support":
                if random() < upgradeChance and tank_and_support_pool:
                    item["id"] = tank_and_support_pool.pop()
                elif allProfession and random() < (upgradeChance * upgradeChance):
                    item["id"] = choice([upgradePool])
                    allProfession = False
            case "sniper" | "medic":
                if random() < upgradeChance and sniper_and_medic_pool:
                    item["id"] = sniper_and_medic_pool.pop()
                elif allProfession and random() < (upgradeChance * upgradeChance):
                    item["id"] = choice([upgradePool])
                    allProfession = False
            case "caster" | "special":
                if random() < upgradeChance and caster_and_special_pool:
                    item["id"] = caster_and_special_pool.pop()
                elif allProfession and random() < (upgradeChance * upgradeChance):
                    item["id"] = choice([upgradePool])
                    allProfession = False
    
    
