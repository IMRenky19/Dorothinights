from ....Model.RogueBase import RogueBasicModel
from ....utils.accounts import decrypt_battle_data
from ..common.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *
from math import floor



async def battleFinish(rogueClass: RogueBasicModel, battleData: str, loginTime: int):
    ts = time()
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    if getCurrentZone(rlv2) == 5 and isZoneEnd(rlv2):
        endGame(rlv2, rlv2_extension)
        rogueClass.rlv2 = rlv2
        rogueClass.extension = rlv2_extension
        return
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
    if pending["content"]["battleReward"]["earn"]["damage"] != 0:
        tmpValue = (1 if rlv2_extension["3_more_chaos"] else 0) + (1 if rlv2_extension["band_11_another_chaos_set"] else 0) + 1
        increaseChaosValue(rlv2, rlv2_extension, tmpValue)
        rlv2["current"]["module"]["chaos"]["lastBattleGain"] = tmpValue
        rlv2["current"]["player"]["property"]["conPerfectBattle"] = 0
    else:
        if rlv2_extension["band_11_another_chaos_set"]:
            increaseChaosValue(rlv2, rlv2_extension, -2)
            rlv2["current"]["module"]["chaos"]["lastBattleGain"] = -2
        rlv2["current"]["player"]["property"]["conPerfectBattle"] += 1
    currentVision = getVision(rlv2)
    if currentVision > 6:
        existence = isRelicExist(rlv2, "rogue_3_relic_fight_22", rlv2_extension)
        if (existence and (getRelicLayer(rlv2, existence[1]) <= 10)) and random() < 0.3:
            addRelicLayer(rlv2, existence[1], 1)
    if currentNodeType == NodeType.ELITE_BATTLE:
        existence = isRelicExist(rlv2, "rogue_3_relic_fight_28",   rlv2_extension)
        if existence and (getRelicLayer(rlv2, existence[1]) <= 15):
            addRelicLayer(rlv2, existence[1], 1)
        existence = isRelicExist(rlv2, "rogue_3_relic_fight_29",   rlv2_extension)
        if existence and (getRelicLayer(rlv2, existence[1]) <= 15):
            addRelicLayer(rlv2, existence[1], 1)
    
    popPending(rlv2)
    addPending(rlv2, pending)
    setCurrentState(rlv2, "PENDING")
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension