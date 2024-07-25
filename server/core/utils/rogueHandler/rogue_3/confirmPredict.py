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

async def confirmPredict(rogueClass: RogueBasicModel):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    setCurrentState(rlv2, "WAIT_MOVE")
    clearAllPending(rlv2)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension