from server.core.utils.rogueHandler.rogue_3.tools.movements import moveTo
from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def moveAndBattleStart(rogueClass: RogueBasicModel, position: dict):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    if not position:
        position = getPosition(rlv2)
    moveTo(rlv2, rlv2_extension, position, getCurrentZone(rlv2))
    setCurrentState(rlv2, "PENDING")
    pending = generateBattlePending(rlv2, rlv2_extension)
    addPending(rlv2, pending)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension