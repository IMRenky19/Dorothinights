from operator import add
from server.core.database.function.userData import getAccountBySecret
from .....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import shuffle, randint, sample
from copy import deepcopy
from server.core.utils.json import read_json
from ..tools.rlv2tools import *
from .map import mapGenerator, visionGenerator
from .battleAndEvent import battleGenerator, eventGenerator, battlePoolGenerator


ts = time()


def moveToNextZone(rlv2_data: dict, rlv2_extension: dict, is_passage = False):
    rlv2_data["current"]["player"]["cursor"]["zone"] += 1
    test = False
    


    if test:
        rlv2_data["current"]["player"]["cursor"].update(
            {
                "zone": 1,
                "position":{
                    "x":2,
                    "y":1
                }
            }
        )
        zone = 114514
    else:
        zone = rlv2_data["current"]["player"]["cursor"]["zone"]
        
    battlePool = battlePoolGenerator(rlv2_data["current"]["player"]["cursor"]["zone"])
    rlv2_data["current"]["map"]["zones"].update(
        battleGenerator(
            visionGenerator(
                rlv2_data["current"]["player"]["cursor"]["zone"],
                getPosition(rlv2_data),
                getVision(rlv2_data),
                mapGenerator(
                    zone, 
                    getNextZoneId(rlv2_data), 
                    alternativeBoss=True,
                    test=test
                )
            ),
            rlv2_data["current"]["player"]["cursor"]["zone"],
            battlePool,
            rlv2_data["current"]["player"]["cursor"]["position"]
        )
    )
    setCurrentState(rlv2_data, "WAIT_MOVE")
    if not is_passage:
        #generatePredict(rlv2_data)
        pass
    else:
        pass
        #todo:)
    if rlv2_extension["3_add_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] == 3:
        addVision(rlv2_data, 1) 
    if rlv2_data["current"]["player"]["cursor"]["zone"] == 1:
        if rlv2_extension["band_13_another_vision_set"]:
            setVision(rlv2_data, 0)
        else:
            setVision(rlv2_data, 3)
            
    if rlv2_extension["12_less_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (1,3,5):
        addVision(rlv2_data, -1)
    if rlv2_extension["band_13_another_vision_set"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (2, 3, 4, 5, 6):
        addVision(rlv2_data, 2)
    
    rlv2_extension.update({
        "battlePool": battlePool
    })
    
    
def moveTo(rlv2_data: dict, rlv2_extension: dict, position: dict, zone: int):
    currentPosition = getPosition(rlv2_data)
    if currentPosition:
        if currentPosition["x"] == position["x"]:
            addVision(rlv2_data, -1)
    rlv2_data["current"]["player"]["cursor"]["position"] = position
    rlv2_data["current"]["player"]["state"] = "PENDING"
    rlv2_data["current"]["player"]["trace"].append(
        {
            "zone": zone,
            "position": position
        }
    )
    print(rlv2_extension["battlePool"])
    rlv2_data["current"]["map"]["zones"].update(
        battleGenerator(
            visionGenerator(
                rlv2_data["current"]["player"]["cursor"]["zone"],
                getPosition(rlv2_data),
                getVision(rlv2_data),
                rlv2_data["current"]["map"]["zones"]
            ),
            rlv2_data["current"]["player"]["cursor"]["zone"],
            rlv2_extension["battlePool"],
            rlv2_data["current"]["player"]["cursor"]["position"]
        )
    )
    