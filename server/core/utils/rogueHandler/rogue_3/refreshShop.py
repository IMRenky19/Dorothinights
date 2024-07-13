from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *

ts = time()

async def refreshShop(rogueClass: RogueBasicModel):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    shop = rlv2["current"]["player"]["pending"][0]["content"]["battleShop"]
    shop["goods"] = generateShopGoods(shop["id"], rlv2, rlv2_extension)
    #shop["refreshCnt"] _= 1
    #TODO:判断当前节点是否为当前层结尾
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension