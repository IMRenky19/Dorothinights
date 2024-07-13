from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from .tools.battleAndEvent import *
from .tools.movements import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_EVENT_DETAILS_PATH
from server.core.utils.time import time
from random import shuffle, randint
import re

ts = time()
rogue_excel = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
rogueEventExcel = read_json(ROGUE_EVENT_DETAILS_PATH)

async def selectChoice(rogueClass: RogueBasicModel, choice: str):
    rlv2_data = getRogueData(rogueClass)
    rlv2ExtensionData = getRogueExtensionData(rogueClass)
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
    
    elif state == "PENDING":    #道中事件
        if choice == "choice_leave":
            setCurrentState(rlv2_data, "WAIT_MOVE")
            clearAllPending(rlv2_data)
            finishNode(rlv2_data)
            zoneEndChecker(rlv2_data, rlv2ExtensionData)
            rogueClass.rlv2 = rlv2_data
            rogueClass.extension = rlv2ExtensionData
            return
        elif getCurrentScene(rlv2ExtensionData) == getCurrentEvent(rlv2ExtensionData):
            #print(getCurrentScene(rlv2ExtensionData))
            choiceInfo = rogueEventExcel["rogue_3"]["Encounter"]["enterScene"][getCurrentScene(rlv2ExtensionData)]["choices"][choice]
            gain = choiceInfo["gain"]
            nextScene = choiceInfo["nextScene"]
            setCurrentScene(rlv2ExtensionData, nextScene)
        elif getCurrentScene(rlv2ExtensionData) != getCurrentEvent(rlv2ExtensionData):
            choiceInfo = rogueEventExcel["rogue_3"]["Encounter"]["others"][getCurrentScene(rlv2ExtensionData)]["choices"][choice]
            gain = choiceInfo["gain"]
            nextScene = choiceInfo["nextScene"]
            setCurrentScene(rlv2ExtensionData, nextScene)
        
        pending = generateNonBattlePending(rlv2_data, rlv2ExtensionData, choice)
        clearAllPending(rlv2_data)
        addPending(rlv2_data, pending)
        for itemType, itemCount in zip([x["itemId"] for x in gain], [x["amount"] for x in gain]):
            match itemType:
                case itemType if itemType.find("gold") != -1:
                    gainItem(rlv2_data, "gold", itemCount)
                case itemType if itemType.find("recruit_ticket") != -1:
                    gainItem(rlv2_data, "recruit_ticket", itemCount, itemType)
                case itemType if itemType.find("totem") != -1:
                    gainItem(rlv2_data, "totem", itemCount, itemType)
                case itemType if itemType.find("vision") != -1:
                    gainItem(rlv2_data, "vision", itemCount)
                case itemType if itemType.find("relic") != -1:
                    gainItem(rlv2_data, "relic", itemCount, itemType, rogueExtension = rlv2ExtensionData)
                case itemType if itemType.find("shield") != -1:
                    gainItem(rlv2_data, "shield", itemCount)
                case itemType if itemType.find("population") != -1:
                    gainItem(rlv2_data, "population", itemCount)
                case itemType if itemType.find("explore_tool") != -1:     #深入调查
                    gainItem(rlv2_data, "explore_tool", itemCount)
                case itemType if itemType.find("active_tool") != -1:        #支援装置       
                    gainItem(rlv2_data, "active_tool", itemCount)
                case itemType if itemType.find("rogue_3_hpmax") != -1:              
                    gainItem(rlv2_data, "hpmax", itemCount)
                case itemType if itemType.find("rogue_3_hp") != -1:              
                    gainItem(rlv2_data, "hp", itemCount)
                case itemType if itemType.find("rogue_3_chaos") != -1:
                    #TODO:坍缩系统
                    pass
                    
    
    rogueClass.rlv2 = rlv2_data
    rogueClass.extension = rlv2ExtensionData
    