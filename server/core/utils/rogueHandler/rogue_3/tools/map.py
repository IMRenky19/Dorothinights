from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_ROUTE_PATH
from random import shuffle, randint, sample, random, choice
from server.core.utils.json import read_json
import re
from enum import Enum
from .tools import *

stage_info: dict = read_json(ROGUELIKE_TOPIC_EXCEL_PATH)["details"]["rogue_3"]["stages"]
route_info: dict = read_json(ROGUE_ROUTE_PATH)

ZONE_1_NORMAL_BATTLE_POOL = ["ro3_n_6_1", "ro3_n_6_2"]
##ZONE_2_NORMAL_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_n_(.*?)_(.*?)", x).group(1)) == 2]
##ZONE_3_NORMAL_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_n_(.*?)_(.*?)", x).group(1)) == 3]
##ZONE_4_NORMAL_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_n_(.*?)_(.*?)", x).group(1)) == 4]
##ZONE_5_NORMAL_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_n_(.*?)_(.*?)", x).group(1)) == 5]
ZONE_6_NORMAL_BATTLE_POOL = ["ro3_n_6_1", "ro3_n_6_2"]
ZONE_1_EMERGENCY_BATTLE_POOL = ["ro3_e_6_1", "ro3_e_6_2"]
##ZONE_2_EMERGENCY_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_e_(.*?)_(.*?)", x).group(1)) == 2]
##ZONE_3_EMERGENCY_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_e_(.*?)_(.*?)", x).group(1)) == 3]
##ZONE_4_EMERGENCY_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_e_(.*?)_(.*?)", x).group(1)) == 4]
##ZONE_5_EMERGENCY_BATTLE_POOL = [x for x in stage_info.keys() if \
##                             int(re.search(r"ro3_e_(.*?)_(.*?)", x).group(1)) == 5]
ZONE_6_EMERGENCY_BATTLE_POOL = ["ro3_e_6_1", "ro3_e_6_2"]

class NodeType(Enum):
    NONE = 1 >> 1
    NORMAL_BATTLE = 1 << 0
    ELITE_BATTLE = 1 << 1
    BOSS = 1 << 2
    PHANTOM_SHOP = 1 << 3
    SAFE_HOUSE = 1 << 4
    ENCOUNTER = 1 << 5
    PHANTOM_TREASURE = 1 << 6
    ENTERTAINMENT = 1 << 7
    UNKNOWN = 1 << 8
    WISH = 1 << 9
    LOST_AND_FOUND = 1 << 10
    SCOUT = 1 << 11
    SHOP = 1 << 12
    PASSAGE = 1 << 13
    MISSION = 1 << 14
    STORY = 1 << 15
    STORY_HIDDEN = 1 << 16
    
class Node:
    def __init__(self, x: int = 0, y: int = 0, visibility: int = 0, nodeType: NodeType = NodeType.NONE, stage = None) -> None:
        self.x = x
        self.y = y
        self.nodeType = nodeType
        self.visibility = visibility
        self.nextNodes = []
        self.stage = stage
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
                "visibility":self.visibility,
                "stage": self.stage
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
    
    
def generateRoute(nodeList: list):                  #todo
    for x_cursor in range(len(nodeList) - 1):
        print(list(range(len(nodeList) - 1)))
        key_front = True
        key_back = True
        if (x_cursor == 0):
            key_front = False
        if (x_cursor == (len(nodeList) - 2)):
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
            if choice([0,0,0,0,1]) and (x_column + 1 <= len(front_column) - 1):
                front_column[x_column].connectToOtherNode(front_column[x_column + 1], key_front)
                front_column[x_column + 1].connectToOtherNode(front_column[x_column], key_front)
    if key_back:
        for i, x_column in zip(back_column, range(len(back_column) - 1)):
            if choice([0,0,0,0,1]) and (x_column + 1 <= len(back_column) - 1):
                back_column[x_column].connectToOtherNode(back_column[x_column + 1], key_back)
                back_column[x_column + 1].connectToOtherNode(back_column[x_column], key_back)
                    

        
def mapGenerator(zone: int, index: int, alternativeBoss: bool = False, end_3: bool = False, \
                    end_4: bool = False, scoutUnlocked: bool = True, passageUnlocked: bool = True, \
                        lostAndFoundUnlocked: bool = True):
    
    total_node = 0
    nodeList = []
    nonBattlePool = []
    battleNodeTotal = 0
    tmpNodeList = []
    eliteBattleTotal = 0
    
    match zone:
        case 1:
            new_map = Map(zone, index)
            eliteBattleTotal = 1
            if random() >= 0.55:
                total_node = 6
            else:
                total_node = 5
            mapMode = randomizePutNode(total_node, 2 ,[[2,3],[2,3]])
            for i in range(total_node):
                if random() >= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = NodeType.NORMAL_BATTLE, stage = choice(ZONE_1_NORMAL_BATTLE_POOL)),
                    Node(0, 1, 0, nodeType = NodeType.NORMAL_BATTLE, stage = choice(ZONE_1_NORMAL_BATTLE_POOL))
                ]
            ]
            
            for i in tmpNodeList:
                for j in i:
                    if nonBattlePool:
                        if random() >= 0.5 and (not battleNodeTotal):
                            j.setNodeType(choice([NodeType.ENCOUNTER]))
                            continue
                    if eliteBattleTotal and random() >= 0.5:
                        j.setNodeType(NodeType.ELITE_BATTLE)
                        j.setStage(choice(ZONE_1_EMERGENCY_BATTLE_POOL))
                        eliteBattleTotal -= 1
                    else:
                        j.setNodeType(NodeType.NORMAL_BATTLE)
                        j.setStage(choice(ZONE_1_NORMAL_BATTLE_POOL))
                        battleNodeTotal -= 1
            nodeList += tmpNodeList
            nodeList.append([
                Node(3, 0, 0, nodeType = NodeType.SHOP),
                Node(3, 1, 0, nodeType = NodeType.SHOP)
            ]
        )
            
            
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
            
            
        case 6:   
            nonBattlePool = [
                    NodeType.SAFE_HOUSE,
                    NodeType.ENTERTAINMENT,
                    NodeType.WISH,
                    NodeType.SHOP,
                    NodeType.PASSAGE,
                    NodeType.ENCOUNTER
                ]
            chance = random()
            if chance >= 0.7:
                total_node = 3
            else:
                total_node = 4
            new_map = Map(zone, index)
            nodeList.append(
                    [Node(0, 0, 0, nodeType = NodeType.SHOP)]
                )
            mapMode = randomizePutNode(total_node, 2, [[1,2],[1,2]])
            tmpNodeList = []
            #x_tmp = 0
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                #y_tmp = 0
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp, y=y_tmp))
                    #y_tmp += 1
                #x_tmp += 1
            #chances_table = [30,26,19,33,26]
            j = 0
            shuffle(nonBattlePool)
            #shuffled = nonBattlePool[0:len(tmpNodeList[1])]
            #shuffled = [choice(nonBattlePool) for k in range(len(tmpNodeList[0]))]
            for i in tmpNodeList[0]:
                i.setNodeType(nonBattlePool[j])
                i.setX(1)
                i.setY(j)
                j += 1
            j = 0
            for i in tmpNodeList[1]:
                i.setNodeType(choice([NodeType.NORMAL_BATTLE, NodeType.ELITE_BATTLE]))
                i.setStage(choice(ZONE_6_NORMAL_BATTLE_POOL) if i.nodeType == NodeType.NORMAL_BATTLE else choice(ZONE_6_EMERGENCY_BATTLE_POOL))
                i.setX(2)
                i.setY(j)
                j += 1
                
            nodeList += tmpNodeList
            nodeList.insert(3, [Node(3, 0, nodeType=NodeType.BOSS)])
            nodeList[3][0].setStage("ro3_b_6" if alternativeBoss else "ro3_b_6")
            #print(nodeList)
                
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        