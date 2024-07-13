from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from ....database.function.userData import getAccountBySecret

ts = time()

async def activeRecruitTicket(rogueClass: RogueBasicModel, choice: str):
    rlv2_data = getRogueData(rogueClass)
    user = await getAccountBySecret(rogueClass.secret)
    userSyncData = user.user
    addRecruitPending(rlv2_data, choice)

    chars = getChars(
        rogueClass.rlv2, 
        rogueClass.extension,
        rlv2_data["current"]["inventory"]["recruit"][choice]["id"], 
        userSyncData
    )
    rlv2_data["current"]["inventory"]["recruit"][choice]["state"] = 1
    rlv2_data["current"]["inventory"]["recruit"][choice]["list"] = chars
    
    
    rogueClass.rlv2 = rlv2_data
    