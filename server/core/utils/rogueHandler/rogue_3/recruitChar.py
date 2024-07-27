from server.core.utils.rogueHandler.rogue_3.tools.battleAndEvent import activateTickets
from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from ..common.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy
from ....database.function.userData import getAccountBySecret

ts = time()

async def recruitChar(rogueClass: RogueBasicModel, ticketId: str, choice: str, isClose = False):
    rlv2Extension = getRogueExtensionData(rogueClass)
    if isClose:
        rlv2 = getRogueData(rogueClass)
        popPending(rlv2)
        rlv2["current"]["inventory"]["recruit"][ticketId]["state"] = 2
        rlv2["current"]["inventory"]["recruit"][ticketId]["list"] = []
    else:
        rlv2 = getRogueData(rogueClass)
        popPending(rlv2)
        char = rlv2["current"]["inventory"]["recruit"][ticketId]["list"][int(choice)]
        isUpgrade = True if char["upgradePhase"] else False
        char_id = getNextCharId(rlv2, rlv2["current"]["inventory"]["recruit"][ticketId]["list"][int(choice)]["charId"], isUpgrade)
        
        char["instId"] = char_id
        rlv2["current"]["inventory"]["recruit"][ticketId]["state"] = 2
        rlv2["current"]["inventory"]["recruit"][ticketId]["list"] = []
        rlv2["current"]["inventory"]["recruit"][ticketId]["result"] = char
        rlv2["current"]["troop"]["chars"][char_id] = char
        rlv2["current"]["player"]["property"]["population"]["cost"] += char["population"]
    
    ticketList = getActivateTicketList(rlv2)
    if ticketList and getCurrentState(rlv2) != "INIT":
        nextTicketId = ticketList.pop(0)
        rogueExtension = getRogueExtensionData(rogueClass)
        userData = await getAccountBySecret(rogueClass.secret)
        userSyncData = userData.user
        activateTickets(rlv2, rlv2["current"]["inventory"]["recruit"][nextTicketId]["id"], userSyncData, rogueExtension, nextTicketId)
        
    rlv2Extension["extraResponse"] = {
        "chars": [rlv2["current"]["inventory"]["recruit"][ticketId]["result"]]
    }
    rlv2Extension["isNewExtraResponse"] = True
    clearExtraResponseData(rlv2, rlv2Extension)
    rogueClass.extension = rlv2Extension
    rogueClass.rlv2 = rlv2
    