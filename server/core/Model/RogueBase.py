from typing import List
from sqlalchemy import Column, Integer, String, JSON, Null
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from .User import Base
from ..utils.time import time

ts = time()

class RogueBasicModel(Base):
    __tablename__ = "rogue"
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    uid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    phone: Mapped[str] = mapped_column(String(255))
    secret: Mapped[str] = mapped_column(String(255))
    
    
    rlv2: Mapped[str] = mapped_column(JSON)
    extension: Mapped[str] = mapped_column(JSON)
    
    def initial_game(self):
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
                    "index": "e_1",
                    "type": "GAME_INIT_RECRUIT_SET",
                    "content": {
                        "initRecruitSet": {
                            "step": [
                                2,
                                3
                            ],
                            "option": recruit_group
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
        rlv2 = initial
    
    #state: Mapped[str] = mapped_column(String(16))
    #exp: Mapped[int] = mapped_column(default=Null)
    #level: Mapped[int] = mapped_column(default=Null)
    #max_level: Mapped[int] = mapped_column(default=Null)
    #hp_current: Mapped[int] = mapped_column(default=Null)
    #hp_max: Mapped[int] = mapped_column(default=Null)
    #gold: Mapped[int] = mapped_column(default=Null)
    #shield: Mapped[int] = mapped_column(default=Null)
    #capacity: Mapped[int] = mapped_column(default=Null)
    #population_cost: Mapped[int] = mapped_column(default=Null)
    #population_max: Mapped[int] = mapped_column(default=Null)
    #conPerfectBattle: Mapped[int] = mapped_column(default=Null)
    #
    #
    #cursor: Mapped[str] = mapped_column(JSON)
    #trace: Mapped[List["Node"]] = relationship(back_populates="user")
    
#class Node(Base):
#    
#    __tablename__ = "node"
#    zone: Mapped[str] = mapped_column(String(16))
#    position: Mapped[str] = mapped_column(JSON)
#    
#    user: Mapped["RogueBase"] = relationship(back_populates="trace")