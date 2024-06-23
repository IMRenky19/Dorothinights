from server.core.database.function.userData import getAccountBySecret
from .....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import shuffle, randint, sample
from copy import deepcopy
from server.core.utils.json import read_json
from .tools import *
from .map import mapGenerator


ts = time()


def moveToNextZone(rlv2_data: dict, rlv2_extension: dict, is_passage = False):
    rlv2_data["current"]["player"]["cursor"]["zone"] += 1
    setCurrentState(rlv2_data, "WAIT_MOVE")
    if not is_passage:
        #generatePredict(rlv2_data)
        pass
    else:
        pass
        #todo:)
    if rlv2_extension["3_add_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] == 3:
        addVision(rlv2_data, 1) 
    if rlv2_extension["12_less_vision"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (1,3,5):
        addVision(rlv2_data, -1)
    if rlv2_data["current"]["player"]["cursor"]["zone"] == 1:
        if rlv2_extension["band_13_another_vision_set"]:
            setVision(rlv2_data, 0)
        else:
            setVision(rlv2_data, 3)
    if rlv2_extension["band_13_another_vision_set"] and rlv2_data["current"]["player"]["cursor"]["zone"] in (2, 3, 4, 5, 6):
        setVision(rlv2_data, 2)

    rlv2_data["current"]["map"]["zones"].update(
        mapGenerator(rlv2_data["current"]["player"]["cursor"]["zone"], getNextZoneId(rlv2_data), alternativeBoss=True))