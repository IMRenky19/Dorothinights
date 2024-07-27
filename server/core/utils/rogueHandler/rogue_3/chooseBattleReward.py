from ....Model.RogueBase import RogueBasicModel
from server.core.database.function.userData import getAccountBySecret
from ..common.rlv2tools import *
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def chooseBattleReward(rogueClass: RogueBasicModel, index: int, sub: int):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    userData = await getAccountBySecret(rogueClass.secret)
    userSyncData = userData.user
    #battleRewardsPending = rlv2["current"]["player"]["pending"]
    #itemType: str = battleRewardsPending[-1]["content"]["battleReward"]["rewards"][index]["items"][sub]["id"]
    #gainItem(rlv2, itemType)
    gainItemsAfterBattle(rlv2, index, sub, userSyncData, rlv2_extension)
    clearExtraResponseData(rlv2, rlv2_extension)
    #TODO:判断当前节点是否为当前层结尾
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension