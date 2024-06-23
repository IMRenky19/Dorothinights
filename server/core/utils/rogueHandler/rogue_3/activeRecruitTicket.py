from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy

ts = time()

async def activeRecruitTicket(rogueClass: RogueBasicModel, choice: str):
    rlv2_data = getRogueData(rogueClass)
    pending_index = getNextPendingIndex(rlv2_data)
    rlv2_data["current"]["player"]["pending"].insert(
        0, {
            "index": pending_index,
            "type": "RECRUIT",
            "content": {
                    "recruit": {
                        "ticket": choice
                    }
            }
        }
    )

    chars = await getChars(rogueClass, [rlv2_data["current"]["inventory"]["recruit"][choice]["id"].split("_")[4]], rogueClass.secret)
    rlv2_data["current"]["inventory"]["recruit"][choice]["state"] = 1
    rlv2_data["current"]["inventory"]["recruit"][choice]["list"] = chars
    
    
    rogueClass.rlv2 = rlv2_data
    