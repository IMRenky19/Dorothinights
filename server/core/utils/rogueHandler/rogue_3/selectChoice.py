from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from .tools.battleAndEvent import *
from .tools.movements import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_EVENT_DETAILS_PATH
from server.core.utils.time import time
from ....database.function.userData import getAccountBySecret
from random import shuffle, randint

import re

ts = time()
rogue_excel = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
rogueEventExcel = read_json(ROGUE_EVENT_DETAILS_PATH)

async def selectChoice(rogueClass: RogueBasicModel, choice: str):
    rlv2_data = getRogueData(rogueClass)
    rlv2ExtensionData = getRogueExtensionData(rogueClass)
    state = getCurrentState(rlv2_data)
    userData = await getAccountBySecret(rogueClass.secret)
    userSyncData = userData.user
    
    
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
            clearExtraResponseData(rlv2_data, rlv2ExtensionData)
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
            gainItem(rlv2_data, itemType, itemCount, itemType,userSyncData = userSyncData, rogueExtension = rlv2ExtensionData)
                
    clearExtraResponseData(rlv2_data, rlv2ExtensionData)
    
    rogueClass.rlv2 = rlv2_data
    rogueClass.extension = rlv2ExtensionData
    