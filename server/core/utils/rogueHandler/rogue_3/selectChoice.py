from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
import re

ts = time()
rogue_excel = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)

async def selectChoice(rogueClass: RogueBasicModel, choice: str):
    rlv2_data = getRogueData(rogueClass)
    state = getCurrentState(rlv2_data)
    
    
    if state == "INIT":   #开局事件
        choice_info = rogue_excel["details"]["rogue_3"]["choices"][choice]
        choice_type = choice_info["icon"]
        match choice_type:
            case "initial_reward_gold":
                num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1)
                addGold(rlv2_data, int(num))
            case "initial_reward_population":
                num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1)
                addPopulation(rlv2_data, int(num))
            case "initial_reward_shield":
                num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1)
                addShield(rlv2_data, int(num))
        rlv2_data["current"]["player"]["pending"].pop(0)
        
    rogueClass.rlv2 = rlv2_data
    