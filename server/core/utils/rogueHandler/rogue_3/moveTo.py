from server.core.utils.rogueHandler.rogue_3.tools.movements import moveTo
from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from .tools.movements import *
from .tools.battleAndEvent import *
from ....database.function.userData import getAccountBySecret

ts = time()

async def rogueMoveTo(rogueClass: RogueBasicModel, position: dict):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    user = await getAccountBySecret(rogueClass.secret)
    userSyncData = user.user
    moveTo(rlv2, rlv2_extension, position, getCurrentZone(rlv2))
    pending = generateNonBattlePending(rlv2, rlv2_extension, None, userSyncData)
    addPending(rlv2, pending)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension