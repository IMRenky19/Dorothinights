from random import shuffle, randint, sample, random, choice
from enum import Enum

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
        if key:
            anotherNode.connectToOtherNode(self, key = key)
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
    return []
    
    
def generateRoute(nodeList: list):
    for x_cursor in range(len(nodeList) - 1):
        tryGenerateRouteBetweenColumn(nodeList[x_cursor], nodeList[x_cursor + 1])
        
                        
def tryGenerateRouteBetweenColumn(front_column: list, back_column: list, key = False):
    
    #没什么用的初始化
    front_column_cursor_y = 0
    back_column_cursor_y = 0
    flag = 0
    
    for j in range(len(front_column)):
        choices_list = [0,1]
        #第一行的节点必定连接，连接后准备判定左侧节点
        if front_column_cursor_y == 0  and back_column_cursor_y == 0:
            front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
            back_column_cursor_y += 1
            
        elif front_column_cursor_y == len(front_column) - 1 and back_column_cursor_y == len(back_column) - 1:
            front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
            break
        #random，下为左侧待连接节点和右侧最后一个被连接的节点的连接判定通过分支
        elif not int(choice([0,1,1,1])):
            front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
            choices_list.append(1)
            choices_list.append(1)
            back_column_cursor_y += 1
        #判定不通过，右侧下个节点必定连接
        else:
            back_column_cursor_y += 1
            flag = 1
        if len(back_column) - 1 < back_column_cursor_y:
            back_column_cursor_y -= 1
            front_column_cursor_y += 1
            continue
        for i in range(len(back_column) - back_column_cursor_y):
            #检测到后列待连接节点为本列最后一个节点，不做random处理直接连接
            if back_column_cursor_y == len(back_column) - 1:
                front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
                front_column_cursor_y += 1
                break
            if front_column_cursor_y == len(front_column) - 1:
                front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
                back_column_cursor_y += 1
                continue
            #正常的条件判断 50%概率判定连接，判定通过则连接节点并设置下一个右侧待连接节点的y坐标
            #（有flag必定连接）
            elif (not int(choice(choices_list)) and len(back_column) - 1 >= back_column_cursor_y) or flag:
                front_column[front_column_cursor_y].connectToOtherNode(back_column[back_column_cursor_y])
                back_column_cursor_y += 1
                choices_list.append(1)
                choices_list.append(1)
            #判定不通过，前列下个节点准备生成连接，后列最后被连接的一个节点加入判定
            else:
                front_column_cursor_y += 1
                back_column_cursor_y -= 1
                break
    

        
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
                            j.setNodeType(choice([NodeType.ENTERTAINMENT]))
                        else:
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
        
        
if __name__ == "__main__":
    print(mapGenerator(1, 1))