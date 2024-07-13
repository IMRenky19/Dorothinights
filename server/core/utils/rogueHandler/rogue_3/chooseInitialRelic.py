from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy

ts = time()

async def chooseInitialRelic(rogueClass: RogueBasicModel, num: int):
    
    rlv2_data = deepcopy(rogueClass.rlv2)
    extension = deepcopy(rogueClass.extension)
    band = rlv2_data["current"]["player"]["pending"][0]["content"]["initRelic"]["items"][num]["id"]
    match band:
        case "rogue_3_band_1": #指挥分队
            addHpLimit(rlv2_data, 2)
            extension["recover_hp_after_battle"] = 1
        case "rogue_3_band_2": #集群分队
            addCapacity(rlv2_data, 2)
            addCharLimit(extension, 2)
        case "rogue_3_band_3": #后勤分队
            addGold(rlv2_data, 20)
            addPopulation(rlv2_data, 2)
        case "rogue_3_band_4": #矛头分队
            setHp(rlv2_data, 1)
            extension["extra_hp"] += 0.15
            extension["extra_atk"] += 0.15
        case "rogue_3_band_5": #突击战术分队
            extension["band_direct_upgrade"] = 1
        case "rogue_3_band_6": #堡垒战术分队
            extension["band_direct_upgrade"] = 2
        case "rogue_3_band_7": #远程战术分队
            extension["band_direct_upgrade"] = 3
        case "rogue_3_band_8": #破坏战术分队
            extension["band_direct_upgrade"] = 4
        case "rogue_3_band_9": #特训分队
            addShield(rlv2_data, 3)
            extension["no_upgrade_population"] = 1
        case "rogue_3_band_11": #永恒狩猎分队
            addHpLimit(rlv2_data, 2)
            addHp(rlv2_data, 2)
            extension["band_11_another_chaos_set"] = 1
        case "rogue_3_band_12": #生活至上分队
            extension["band_12_totems"] = 1
        case "rogue_3_band_13": #科学主义分队
            extension["band_13_another_vision_set"] = 1
        
    rlv2_data["current"]["player"]["pending"].pop(0)
    rlv2_data["current"]["inventory"]["relic"]["r_0"] = {
        "index": "r_0",
        "id": band,
        "count": 1,
        "ts": ts
    }
    
    rogueClass.rlv2 = rlv2_data
    rogueClass.extension = extension
