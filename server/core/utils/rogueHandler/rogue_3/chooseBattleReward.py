from server.core.utils.rogueHandler.rogue_3.tools.movements import moveTo
from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ....utils.accounts import decrypt_battle_data
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def chooseBattleReward(rogueClass: RogueBasicModel, index: int, sub: int):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    gainItemsAfterBattle(rlv2, index, sub)
    #TODO:判断当前节点是否为当前层结尾
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension