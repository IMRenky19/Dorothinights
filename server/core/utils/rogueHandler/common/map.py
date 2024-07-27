from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_ROUTE_PATH
from random import shuffle, randint, sample, random, choice
from server.core.utils.json import read_json
import re
from enum import IntEnum


route_info: dict = read_json(ROGUE_ROUTE_PATH)

class NodeType(IntEnum):
    NONE = 1 >> 1               #无
    NORMAL_BATTLE = 1 << 0      #普通作战
    ELITE_BATTLE = 1 << 1       #紧急作战
    BOSS = 1 << 2               #险路恶敌
    PHANTOM_SHOP = 1 << 3       #商店（傀影ver.）
    SAFE_HOUSE = 1 << 4         #安全的角落
    ENCOUNTER = 1 << 5          #不期而遇
    PHANTOM_TREASURE = 1 << 6   #古堡馈赠
    ENTERTAINMENT = 1 << 7      #兴致盎然
    UNKNOWN = 1 << 8            #迷雾重重
    WISH = 1 << 9               #得偿所愿
    LOST_AND_FOUND = 1 << 10    #失与得/风雨际会
    SCOUT = 1 << 11             #先行一步/紧急运输
    SHOP = 1 << 12              #诡意行商
    PASSAGE = 1 << 13           #误入奇境/树篱之途/思维边界
    MISSION = 1 << 14           #地区委托
    STORY = 1 << 15             #命运所指（萨米肉鸽一二四结局，萨卡兹肉鸽）
    STORY_HIDDEN = 1 << 16      #命运所指（萨米肉鸽三结局）
    ALCHEMY = 1 << 17           #去伪存真
    DUEL = 1 << 18              #狭路相逢
    
class Node:
    def __init__(self, x: int = 0, y: int = 0, visibility: int = 0, \
        nodeType: NodeType = NodeType.NONE, stage = None, isZoneEnd = False) -> None:
        self.x = x
        self.y = y
        self.nodeType = nodeType
        self.visibility = visibility
        self.nextNodes = []
        self.stage = stage
        self.zone_end = isZoneEnd
    def connectToOtherNode(self, anotherNode, key: bool = False):
        self.nextNodes.append(
            {
                "x": anotherNode.x,
                "y": anotherNode.y,
                "key": key
            }
        )
    def setNodeType(self, nodeType: NodeType):
        self.nodeType = nodeType
    def setX(self, x: int):
        self.x = x
    def setY(self, y: int):
        self.y = y
    def setVisibility(self, visibility: int):
        self.visibility = visibility
    def setStage(self, stage: str):
        self.stage = stage
    def exportNode(self):
        index = f"{self.x}0{self.y}" if self.x != 0 else f"{self.y}"
        return {
            index:{
                "index":index,
                "pos":{
                    "x":self.x,
                    "y":self.y
                },
                "next":self.nextNodes,
                "type":self.nodeType,
                "realNodeType":self.nodeType,
                "visibility":self.visibility,
                "stage": self.stage,
                "zone_end": self.zone_end,
                "alwaysVisible": False,
                "attach": []
            }
        }
        
class Map:
    def __init__(self, zone: int, index: int) -> None:
        self.zone = zone
        self.index = index
        self.nodes = {}
        
    
    def addNode(self, newNode: Node):
        self.nodes.update(
            newNode.exportNode()
        )
        
        
    def exportMap(self):
        return {
            str(self.zone): {
                "id":f"zone_{self.zone}",
                "index":self.index,
                "nodes":self.nodes
            }
        }

def randomizePutNode(total: int, column_amount: int, column_min_and_max_node: list) -> list:
    before_first_try = [randint(column_min_and_max_node[x][0], column_min_and_max_node[x][1]) \
        for x in range(column_amount - 1)]
    last_column = total - sum(before_first_try)
    if (last_column <= column_min_and_max_node[column_amount - 1][1]) and \
        (last_column >= column_min_and_max_node[column_amount - 1][0]):
        before_first_try.append(last_column)
        return before_first_try
    
    if (last_column > column_min_and_max_node[column_amount - 1][1]):
        index = 0
        modify_3 = []
        for i in column_min_and_max_node[0:-1]:
            i[0] = 0
            i[1] = column_min_and_max_node[index][1] - before_first_try[index]
            index += 1
            modify_3.append(i)
        modified = randomizePutNode(last_column - column_min_and_max_node[column_amount - 1][1],
                         column_amount - 1, modify_3)
        for a, b in zip(list(range(len(before_first_try))), list(range(len(modified)))):
            before_first_try[a] += modified[b]
        before_first_try.append(column_min_and_max_node[column_amount - 1][1])
        return before_first_try
    if (last_column < column_min_and_max_node[column_amount - 1][0]):
        index = 0
        modify_3 = []
        for i in column_min_and_max_node[0:-1]:
            i[0] = 0
            i[1] = before_first_try[index] - column_min_and_max_node[index][0]
            index += 1
            modify_3.append(i)
        maximal_index = modify_3.index(max(modify_3))
        before_first_try[maximal_index] -= (column_min_and_max_node[column_amount - 1][0] - last_column)
        last_column = column_min_and_max_node[column_amount - 1][0]
        before_first_try.append(column_min_and_max_node[column_amount - 1][1])
        return before_first_try
    return []
    
    
def generateRoute(nodeList: list, five = False):                  #todo
    for x_cursor in range(len(nodeList) - 1):
        key_front = False
        key_back = True
        if (x_cursor == 0) or ((x_cursor == 4) and five):
            key_front = False
        if (x_cursor == (len(nodeList) - 2)) or ((x_cursor == 3) and five):
            key_back = False
        tryGenerateRouteBetweenColumn(nodeList[x_cursor], nodeList[x_cursor + 1], key_front, key_back)
        
                        
def tryGenerateRouteBetweenColumn(front_column: list, back_column: list, key_front = False, key_back = False):
    front_len = len(front_column)
    back_len = len(back_column)
    mode = str(front_len) + "-" + str(back_len)
    
    mode_set = choice(route_info[mode])
    for front_y_column, back_y_column_list in zip(mode_set[0], mode_set[1]):
        for back_y_column in back_y_column_list:
            front_column[front_y_column - 1].connectToOtherNode(back_column[back_y_column - 1])
    if key_front:
        for i, x_column in zip(front_column, range(len(front_column) - 1)):
            if choice([0,1]) and (x_column + 1 <= len(front_column) - 1):
                front_column[x_column].connectToOtherNode(front_column[x_column + 1], key_front)
                front_column[x_column + 1].connectToOtherNode(front_column[x_column], key_front)
    if key_back:
        for i, x_column in zip(back_column, range(len(back_column) - 1)):
            if choice([0,1]) and (x_column + 1 <= len(back_column) - 1):
                back_column[x_column].connectToOtherNode(back_column[x_column + 1], key_back)
                back_column[x_column + 1].connectToOtherNode(back_column[x_column], key_back)

