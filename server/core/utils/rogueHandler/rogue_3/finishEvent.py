from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from .tools.movements import moveToNextZone
ts = time()


async def rlv2FinishEvent(rogueData: RogueBasicModel):
    rlv2 = getRogueData(rogueData)
    rlv2_extension = getRogueExtensionData(rogueData)
    moveToNextZone(rlv2, rlv2_extension)
    popPending(rlv2)
    
    rogueData.rlv2 = rlv2
    rogueData.extension = rlv2_extension
    