from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.tools import getInnerBuffs, getOutBuffs
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint


ts = time()

def createGameBase():
        initial = {
        "player": {
            "state": "INIT",
            "property": {
                "exp": 0,
                "level": 1,
                "maxLevel": 10,
                "hp": {
                    "current": 8,
                    "max": 8
                },
                "gold": 6,
                "shield": 0,
                "capacity": 6,
                "population": {
                    "cost": 0,
                    "max": 6
                },
                "conPerfectBattle": 0
            },
            "cursor": {
                "zone": 0,
                "position": None
            },
            "trace": [],
            "pending": [
                {
                    "index": "e_0",
                    "type": "GAME_INIT_RELIC",
                    "content": {
                        "initRelic": {
                            "step": [
                                1,
                                3
                            ],
                            "items": {}
                        }
                    }
                },
                {
                    "index": "e_1",
                    "type": "GAME_INIT_RECRUIT_SET",
                    "content": {
                        "initRecruitSet": {
                            "step": [
                                2,
                                3
                            ],
                            "option": {}
                        }
                    }
                },
                {
                    "index": "e_2",
                    "type": "GAME_INIT_RECRUIT",
                    "content": {
                        "initRecruit": {
                            "step": [
                                3,
                                3
                            ],
                            "tickets": [],
                            "showChar": [],
                            "team": None
                        }
                    }
                }
            ],
            "status": {
                "bankPut": 0
            },
            "toEnding": None,
            "chgEnding": False
        },
        "record": {
            "brief": None
        },
        "map": {
            "zones": {}
        },
        "troop": {
            "chars": {},
            "expedition": [],
            "expeditionReturn": None,
            "hasExpeditionReturn": False
        },
        "inventory": {
            "relic": {},
            "recruit": {},
            "trap": None,
            "consumable": {},
            "exploreTool": {}
        },
        "game": {
            "mode": None,
            "predefined": None,
            "theme": None,
            "outer": {
                "support": False
            },
            "start": ts,
            "modeGrade": None,
            "equivalentGrade": None
        },
        "buff": {
            "tmpHP": 0,
            "capsule": None,
            "squadBuff": []
        },
        "module":{}
    }
        return initial

def createGame(hardLevel: int, rogueClass: RogueBasicModel):
    base_data = createGameBase()
    return base_data
    
async def createGameExtra(rogueClass: RogueBasicModel, hardLevel: int):
    rlv2_table = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
    bands = rlv2_table["details"]["rogue_3"]["init"][0]["initialBandRelic"]
    initial = createGame(hardLevel, rogueClass)
    have_init_support = 1
    getOutBuffs(rogueClass)
    getInnerBuffs(rogueClass, hardLevel)
    initial["player"]["property"].update(
        {
            "gold": 6 + rogueClass.extension["extra_gold"],
            "capacity": 6 + rogueClass.extension["extra_capacity"],
            "hp": {
                "current": 8 + rogueClass.extension["extra_hp_limit"],
                "max": 8 + rogueClass.extension["extra_hp_limit"]
            },
            "hpShowState": "NORMAL"
        }
    )
    initial["player"].update(
            {
                "pending": [
                    
                        {
                            "index": "e_0",
                            "type": "GAME_INIT_RELIC",
                            "content": {
                                "initRelic": {
                                    "step": [
                                        1,
                                        3 + have_init_support
                                    ],
                                    "items": {
                                        str(i): {
                                            "id": band,
                                            "count": 1
                                        } for i, band in enumerate(bands)
                                    }
                                }
                            }
                        },
                        {
                            "index": f"e_{1 + have_init_support}",
                            "type": "GAME_INIT_RECRUIT_SET",
                            "content": {
                                "initRecruitSet": {
                                    "step": [
                                        2 + have_init_support,
                                        3 + have_init_support
                                    ],
                                    "option": ["recruit_group_1","recruit_group_2","recruit_group_3","recruit_group_random"]
                                }
                            }
                        },
                        {
                            "index": f"e_{2 + have_init_support}",
                            "type": "GAME_INIT_RECRUIT",
                            "content": {
                                "initRecruit": {
                                    "step": [
                                        3 + have_init_support,
                                        3 + have_init_support
                                    ],
                                    "tickets": [],
                                    "showChar": [],
                                    "team": None
                                }
                            }
                        }
                        
                    
                ],
                "toEnding": "ro3_ending_1",
                "chgEnding": False
            }
    )
    print(1)
    if have_init_support:
        print(114)
        choiceList = [
            "choice_ro3_startbuff_1",
            "choice_ro3_startbuff_2",
            "choice_ro3_startbuff_3"
        ]
        shuffle(choiceList)
        initial["player"]["pending"].insert(1,
            {
                "index": "e_1",
                "type": "GAME_INIT_SUPPORT",
                "content": {
                    "initSupport": {
                        "step": [
                            2,
                            4
                        ],
                        "scene": {
                            "id": "scene_ro3_startbuff_enter",
                            "choices": {x:1 for x in choiceList}
                        }
                    }
                }
            })
    
    ts = time()
    
    initial.update(
        {
            "game": {
                "mode": "NORMAL",
                "predefined": None,
                "theme": "rogue_3",
                "outer": {
                    "support": True
                },
                "start": ts,
                "modeGrade": hardLevel,
                "equivalentGrade": hardLevel
            },
            "module": {
                "chaos": {
                    "level": 0,
                    "value": 0,
                    "curMaxValue": 4,
                    "chaosList": [],
                    "deltaChaos": {
                        "preLevel": 0,
                        "afterLevel": 0,
                        "dValue": 0,
                        "dChaos": []
                    },
                    "lastBattleGain": 0
                },
                "totem": {
                    "totemPiece": []
                },
                "vision": {
                    "value": 0,
                    "isMax": False
                }
            }
        },
        
    )
    rogueClass.rlv2["current"] = initial