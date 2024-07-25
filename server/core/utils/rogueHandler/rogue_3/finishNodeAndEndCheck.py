from server.core.utils.rogueHandler.rogue_3.tools.movements import moveTo
from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ....utils.accounts import decrypt_battle_data
from ..common.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def finishNodeAndEndCheck(rogueClass: RogueBasicModel):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    if rlv2["current"]["map"]["zones"][str(getCurrentZone(rlv2))]["nodes"][positionToIndex(getPosition(rlv2))]["type"] in [NodeType.NORMAL_BATTLE, NodeType.ELITE_BATTLE, NodeType.BOSS]:
        pending = rlv2["current"]["player"]["pending"][0]
        if isRelicExist(rlv2, "rogue_3_relic_legacy_173", rlv2_extension):
            addHp(rlv2, -2),
            addPopulation(rlv2, 1)
            addGold(rlv2, 5)
        if pending["content"]["battleReward"]["earn"]["damage"] != 0:
            tmpValue = (1 if rlv2_extension["3_more_chaos"] else 0) + (1 if rlv2_extension["band_11_another_chaos_set"] else 0) + 1
            increaseChaosValue(rlv2, rlv2_extension, tmpValue)
            rlv2["current"]["module"]["chaos"]["lastBattleGain"] = tmpValue
        else:
            if rlv2_extension["band_11_another_chaos_set"]:
                increaseChaosValue(rlv2, rlv2_extension, -2)
                rlv2["current"]["module"]["chaos"]["lastBattleGain"] = -2
            if getHp(rlv2) > 10 and rlv2_extension["add_shield"] and rlv2["current"]["player"]["property"]["conPerfectBattle"]:
                addShield(rlv2, 1)
    setCurrentState(rlv2, "WAIT_MOVE")
    clearAllPending(rlv2)    
    zoneEndChecker(rlv2, rlv2_extension)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension