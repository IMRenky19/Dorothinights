from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from server.core.database.function.userData import getAccountBySecret
from .tools.movements import moveToNextZone
ts = time()


async def rlv2FinishEvent(rogueData: RogueBasicModel):
    rlv2 = getRogueData(rogueData)
    rlv2_extension = getRogueExtensionData(rogueData)
    user = await getAccountBySecret(rogueData.secret)
    userSyncData = user.user
    moveToNextZone(rlv2, rlv2_extension, userSyncData)
    popPending(rlv2)
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueData.rlv2 = rlv2
    rogueData.extension = rlv2_extension
    