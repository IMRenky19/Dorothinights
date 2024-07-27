from server.core.database.function import rogueData
from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from server.core.database.function.userData import getAccountBySecret
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def buyGoods(rogueClass: RogueBasicModel, choice: int):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    userData = await getAccountBySecret(rogueClass.secret)
    userSyncData = userData.user
    shop = rlv2["current"]["player"]["pending"][0]["content"]["battleShop"]
    chosenItem = shop["goods"][choice]
    addGold(rlv2, -(chosenItem["priceCount"]))
    gainItem(rlv2, chosenItem["itemId"], 1, chosenItem["itemId"], userSyncData, rlv2_extension)
    
    if isRelicExist(rlv2, "rogue_3_relic_explore_2", rlv2_extension):   #TODO：失与得部分
        addPopulation(rlv2, 1)
        
    chosenItem["count"] -= 1
    #TODO:判断当前节点是否为当前层结尾
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension