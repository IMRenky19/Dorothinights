from random import shuffle, random, choice
from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_MODULE_DATA_PATH, ROGUE_RELIC_POOL_PATH
from server.core.utils.json import read_json
from server.core.utils.rogueHandler.rogue_3.tools.totemAndChaos import deepenChaos, increaseChaosValue

from ... import common
from ...common import NodeType


from ...common.rlv2tools import *

roguePoolTable = read_json(ROGUE_RELIC_POOL_PATH)
rogueModuleTable = read_json(ROGUE_MODULE_DATA_PATH)
rogueTable = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)


