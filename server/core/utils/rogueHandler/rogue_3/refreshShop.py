from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time
from .tools.movements import *
from .tools.battleAndEvent import *
from server.constants import ROGUE_SETTING_PATH

ts = time()
setting = read_json(ROGUE_SETTING_PATH)

async def refreshShop(rogueClass: RogueBasicModel):
    rlv2 = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    shop = rlv2["current"]["player"]["pending"][0]["content"]["battleShop"]
    shop["goods"] = generateShopGoods(shop["id"], rlv2, rlv2_extension)
    if not setting["shopRefreshTest"]:
        shop["refreshCnt"] -= 1
    #shop["refreshCnt"] _= 1
    #TODO:判断当前节点是否为当前层结尾
    clearExtraResponseData(rlv2, rlv2_extension)
    rogueClass.rlv2 = rlv2
    rogueClass.extension = rlv2_extension