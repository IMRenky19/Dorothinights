from ....Model.RogueBase import RogueBasicModel
from ..common.rlv2tools import *
from server.core.utils.time import time

ts = time()


async def chooseInitialRecruitSet(rogueClass: RogueBasicModel, select: str):
    
    rlv2_data = getRogueData(rogueClass)
    rlv2_extension = getRogueExtensionData(rogueClass)
    rlv2_data["current"]["player"]["pending"].pop(0)
    
    match select:
        case "recruit_group_1":
            for profession in ["pioneer","sniper","special"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data, ticket_id, True, profession)
        case "recruit_group_2":
            for profession in ["tank","caster","sniper"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data, ticket_id, True, profession)
        case "recruit_group_3":
            for profession in ["warrior","support","medic"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data, ticket_id, True, profession)
        case "recruit_group_random":
            pass
    clearExtraResponseData(rlv2_data, rlv2_extension)
        
    rogueClass.rlv2 = rlv2_data
    rogueClass.extension = rlv2_extension
