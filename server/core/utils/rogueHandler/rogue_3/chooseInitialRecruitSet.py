from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint

ts = time()


async def chooseInitialRecruitSet(rogueClass: RogueBasicModel, select: str):
    
    rlv2_data = getRogueData(rogueClass)
    rlv2_data["current"]["player"]["pending"].pop(0)
    
    match select:
        case "recruit_group_1":
            for profession in ["pioneer","sniper","special"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data["current"], ticket_id, True, profession)
        case "recruit_group_2":
            for profession in ["tank","caster","sniper"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data["current"], ticket_id, True, profession)
        case "recruit_group_3":
            for profession in ["warrior","support","medic"]:
                ticket_id = getNextTicketIndex(rlv2_data)
                addTicket(rlv2_data["current"], ticket_id, True, profession)
        case "recruit_group_random":
            pass
        
        
    rogueClass.rlv2 = rlv2_data
