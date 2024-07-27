from server.core.utils.rogueHandler.common.rlv2tools import getCurrentZone, getTheme
from server.core.utils.time import time
from .rlv2tools import *
from .battleAndEvent import battlePoolGenerator, eventPoolGenerator


ts = time()


def moveToNextZone(rlv2_data: dict, rlv2_extension: dict, isHiddenZone = False):
    theme = getTheme(rlv2_data)
    rlv2_data["current"]["player"]["cursor"]["zone"] += 1
    rlv2_extension["realZone"] += 1
    zone = getCurrentZone(rlv2_data)
    rlv2_data["current"]["player"]["cursor"]["position"] = None
    battlePool = battlePoolGenerator(zone, theme)
    eventPool = eventPoolGenerator(rlv2_extension["realZone"], rlv2_extension["eventPool"], theme)
    setCurrentState(rlv2_data, "WAIT_MOVE")
    rlv2_extension.update({
        "battlePool": battlePool,
        "eventPool": eventPool
    })
    return [battlePool, eventPool]
    
def moveTo(rlv2_data: dict, rlv2_extension: dict, position: dict, zone: int):
    rlv2_data["current"]["player"]["cursor"]["position"] = position
    rlv2_data["current"]["player"]["state"] = "PENDING"
    rlv2_data["current"]["player"]["trace"].append(
        {
            "zone": zone,
            "position": position
        }
    )
    
    
    