from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from .tools.battleAndEvent import *
from .tools.movements import *
from server.constants import ROGUE_BATTLE_POOL_PATH, ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_EVENT_DETAILS_PATH
from server.core.utils.time import time
from ....database.function.userData import getAccountBySecret
from random import shuffle
from random import choice as randomPick

import re

ts = time()
rogue_excel = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)
rogueEventExcel = read_json(ROGUE_EVENT_DETAILS_PATH)
rogueBattlePool = read_json(ROGUE_BATTLE_POOL_PATH)

async def selectChoice(rogueClass: RogueBasicModel, choice: str):
    rogueData = getRogueData(rogueClass)
    rogueExtension = getRogueExtensionData(rogueClass)
    user = await getAccountBySecret(rogueClass.secret)
    userSyncData = user.user
    state = getCurrentState(rogueData)
    userData = await getAccountBySecret(rogueClass.secret)
    userSyncData = userData.user
    gain = []
    nextScene = ""
    
    if state == "INIT":   #开局事件
        choice_info = rogue_excel["details"]["rogue_3"]["choices"][choice]
        choice_type = choice_info["icon"]
        match choice_type:
            case "initial_reward_gold":
                #num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1) #TODO
                num = 5
                addGold(rogueData, int(num))
            case "initial_reward_population":
                #num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1)
                num = 2
                addPopulation(rogueData, int(num))
            case "initial_reward_shield":
                #num = re.search(r"<@ro3.get>(.*?)</>", choice_info["description"]).group(1)
                num = 3
                addShield(rogueData, int(num))
        rogueData["current"]["player"]["pending"].pop(0)
    
    elif state == "PENDING":    #道中事件
        currentNodeType = getNodeType(rogueData)
        nodeTypeStr = ""
        match currentNodeType:
            case currentNodeType if currentNodeType == NodeType.ENCOUNTER:
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.LOST_AND_FOUND:
                #nodeTypeStr = "Sacrifice"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.SAFE_HOUSE:
                #nodeTypeStr = "SafeHouse"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.PASSAGE:
                #nodeTypeStr = "Passage"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.ENTERTAINMENT:
                #nodeTypeStr = "Entertainment"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.SCOUT:
                #nodeTypeStr = "Expedition"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType == NodeType.WISH:
                #nodeTypeStr = "Wish"
                nodeTypeStr = "Encounter"
            case currentNodeType if currentNodeType in [NodeType.STORY, NodeType.STORY_HIDDEN]:
                #nodeTypeStr = "Prophecy"
                nodeTypeStr = "Encounter"
        if choice == "choice_leave":
            setCurrentState(rogueData, "WAIT_MOVE")
            gain = []
            clearAllPending(rogueData)
            finishNode(rogueData)
            zoneEndChecker(rogueData, rogueExtension, userSyncData)
            clearExtraResponseData(rogueData, rogueExtension)
            rogueClass.rlv2 = rogueData
            rogueClass.extension = rogueExtension
            return
        elif getCurrentScene(rogueExtension) == getCurrentEvent(rogueExtension):
            eventType = "enterScene"
            choiceInfo = rogueEventExcel["rogue_3"][nodeTypeStr]["enterScene"][getCurrentScene(rogueExtension)]["choices"][choice]
            gain = choiceInfo["gain"]
            nextScene = choiceInfo["nextScene"]
            setCurrentScene(rogueExtension, nextScene)
        elif getCurrentScene(rogueExtension) != getCurrentEvent(rogueExtension):
            eventType = "others"
            choiceInfo = rogueEventExcel["rogue_3"][nodeTypeStr]["others"][getCurrentScene(rogueExtension)]["choices"][choice]
            gain = choiceInfo["gain"]
            nextScene = choiceInfo["nextScene"]
            setCurrentScene(rogueExtension, nextScene)
        else:
            return
        
        pending = rogueData["current"]["player"]["pending"][0]
        
        for gainDetail in gain:
            itemType = gainDetail["itemId"]
            itemCount = gainDetail["amount"]
            if itemCount == -1:
                ret = isRelicExist(rogueData, itemType, rogueExtension)
                removeRelic(rogueData, rogueExtension, ret[1])
            else:
                if pending["content"]["scene"]["choiceAdditional"][choice]["rewards"]:
                    itemId = pending["content"]["scene"]["choiceAdditional"][choice]["rewards"][0]["id"]
                    gainItem(
                        rogueData, 
                        itemId, 
                        itemCount, 
                        itemId,
                        userSyncData = userSyncData, 
                        rogueExtension = rogueExtension
                    )
                    
            match itemType:    
                case "RANDOM_RELIC":
                    hasRelicInfo = rogueData["current"]["inventory"]["relic"]
                    hasRelic = [itemType for x in hasRelicInfo.values()]
                    relics = [i for i in roguePoolTable["rogue_3"][gainDetail["pool"]] if not (i in hasRelic)]
                    items = []
                    itemsId = []
                    for i in range(itemCount):
                        shuffle(relics)
                        relic = relicLevelCheck(relics.pop(), rogueExtension)
                        gainItem(rogueData, relic, 1, relic, userSyncData, rogueExtension)
                        items.append(
                            {
                                "id": relic,
                                "count": 1
                            }
                        )
                        itemsId.append(relic)
                    writeExtraResponseData(
                        rogueData, 
                        rogueExtension, 
                        {
                            "items": items,
                            "pushMessage":[
                                {
                                    "path":"rlv2GotRandRelic",
                                    "payload":{
                                        "idList":itemsId
                                    }
                                }
                            ]
                        }
                    )
                case "RANDOM_TOTEM":
                    items = []
                    itemsId = []
                    randomTotemId = randomPick(roguePoolTable["rogue_3"]["totemAll"])
                    items.append(
                        {
                            "id": randomTotemId,
                            "count": 1
                        }
                    )
                    itemsId.append(randomTotemId)
                    writeExtraResponseData(
                        rogueData, 
                        rogueExtension, 
                        {
                            "items": items,
                            "pushMessage":[
                                {
                                    "path":"rlv2GotRandRelic",
                                    "payload":{
                                        "idList":itemsId
                                    }
                                }
                            ]
                        }
                    )
                case "RELIC":
                    gainItem(rogueData, gainDetail["relicId"], itemCount, itemType,userSyncData = userSyncData, rogueExtension = rogueExtension)
                case "flag":
                    rogueExtension["eventFlag"].append(gainDetail["flagId"])
                case _: 
                    gainItem(rogueData, itemType, itemCount, itemType,userSyncData = userSyncData, rogueExtension = rogueExtension)
        if nextScene.find("BATTLE") != -1:
            currentNode = rogueData["current"]["map"]["zones"][str(getCurrentZone(rogueData))]["nodes"][positionToIndex(getPosition(rogueData))]
            if type(choiceInfo["battlePool"]) == str:
                currentNode["stage"] = choiceInfo["battlePool"]
            else:
                currentNode["stage"] = randomPick(rogueBattlePool["rogue_3"][f"ZONE_{choiceInfo["battlePool"]}_{'EMERGENCY' if nextScene.find("ELITE") else 'NORMAL'}_BATTLE_POOL"])
            pending = generateBattlePending(rogueData, rogueExtension, isEventBattle = True)
            clearAllPending(rogueData)
            addPending(rogueData, pending)
            clearExtraResponseData(rogueData, rogueExtension)
            rogueClass.rlv2 = rogueData
            rogueClass.extension = rogueExtension
            return
        pending = generateNonBattlePending(rogueData, rogueExtension, choice, userSyncData)
        clearAllPending(rogueData)
        addPending(rogueData, pending)      
    clearExtraResponseData(rogueData, rogueExtension)
    
    rogueClass.rlv2 = rogueData
    rogueClass.extension = rogueExtension
    