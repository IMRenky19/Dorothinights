from ....Model.RogueBase import RogueBasicModel
from ....utils.json import read_json
from .tools.rlv2tools import *
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH
from server.core.utils.time import time
from random import shuffle, randint
from copy import deepcopy

ts = time()

async def recruitChar(rogueClass: RogueBasicModel, ticketId: str, choice: str):

    rlv2 = getRogueData(rogueClass)
    rlv2["current"]["player"]["pending"].pop(0)
    char_id = getNextCharId(rlv2)
    char = rlv2["current"]["inventory"]["recruit"][ticketId]["list"][int(choice)]
    char["instId"] = char_id
    rlv2["current"]["inventory"]["recruit"][ticketId]["state"] = 2
    rlv2["current"]["inventory"]["recruit"][ticketId]["list"] = []
    rlv2["current"]["inventory"]["recruit"][ticketId]["result"] = char
    rlv2["current"]["troop"]["chars"][char_id] = char
    rlv2["current"]["player"]["property"]["population"]["cost"] += char["population"]

    rogueClass.rlv2 = rlv2