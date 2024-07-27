from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def confirmPredict(rogueClass: RogueBasicModel):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    setCurrentState(rlv2, "WAIT_MOVE")
    clearAllPending(rlv2)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension