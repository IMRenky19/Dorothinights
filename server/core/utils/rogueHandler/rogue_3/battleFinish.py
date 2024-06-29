from server.core.utils.rogueHandler.rogue_3.tools.movements import moveTo
from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ....utils.accounts import decrypt_battle_data
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from .tools.movements import *
from .tools.battleAndEvent import *
from math import floor
from .tools.map import NodeType



async def battleFinish(rogueClass: RogueBasicModel, battleData: str, loginTime: int):
    ts = time()
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    decryptedBattleData = decrypt_battle_data(battleData, loginTime)
    #print(decryptedBattleData)
    currentZone = getCurrentZone(rlv2)
    currentNode = rlv2["current"]["map"]["zones"]\
        [str(currentZone)]["nodes"][str(positionToIndex(getPosition(rlv2)))]
    currentNode["fts"] = ts
    currentNodeType = currentNode["realNodeType"]
    currentNodeStage = currentNode["stage"]
    gainGold = 0
    gainExp = 0
    match currentZone:
        case 1:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(10 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 2
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp += floor(12 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 3
        case 2:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(12 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 2
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp += floor(18 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 3
        case 3:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(14 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 2
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp += floor(24 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 4
            elif currentNodeType == NodeType.BOSS:
                if currentNodeStage in ["ro3_b_3_b", "ro3_b_2_b", "ro3_b_1_b"]:
                    gainExp += floor(36 * (1 + rlv2_extension["extra_exp"]))
                    gainGold += 6
                else:
                    gainExp += floor(32 * (1 + rlv2_extension["extra_exp"]))
                    gainGold += 5
        case 4:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(16 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 3
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp += floor(30 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 4
        case 5:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(20 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 3
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp += floor(36 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 5
            elif currentNodeType == NodeType.BOSS:
                gainExp += floor(50 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 7
                
        case 6:
            if currentNodeType == NodeType.NORMAL_BATTLE:
                gainExp += floor(20 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 3
            elif currentNodeType == NodeType.ELITE_BATTLE:
                gainExp +=floor(36 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 5
            elif currentNodeType == NodeType.BOSS:
                gainExp += floor(70 * (1 + rlv2_extension["extra_exp"]))
                gainGold += 8
        case 7:
            pass
    pending = generateBattleRewardPending(rlv2, rlv2_extension, currentNodeStage, \
        currentNodeType, decryptedBattleData, gainExp, gainGold)
    popPending(rlv2)
    addPending(rlv2, pending)
    setCurrentState(rlv2, "PENDING")
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension