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
                "zone_end": self.zone_end
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
                    

        
"""def mapGenerator(zone: int, index: int, alternativeBoss: bool = False, end_3: bool = False, \
                    end_4: bool = False, scoutUnlocked: bool = True, passageUnlocked: bool = True, \
                        lostAndFoundUnlocked: bool = True, test = False):
    
    total_node = 0
    nodeList = []
    nonBattlePool = []
    battleNodeTotal = 0
    tmpNodeList = []
    eliteBattleTotal = 0
        
    match zone:
        case 1:                    #1
            wish_gen = True
            entertainment_gen = True
            new_map = Map(zone, index)
            eliteBattleTotal = 1
            if random() >= 0.55:
                total_node = 6
            else:
                total_node = 5
            mapMode = randomizePutNode(total_node, 2 ,[[2,3],[2,3]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.15 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.02 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = NodeType.NORMAL_BATTLE),
                    Node(0, 1, 0, nodeType = NodeType.NORMAL_BATTLE)
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0.5
                else:
                    random_chance = 0.5
                for j in i:
                    if (random() <= random_chance or (not nonBattlePool)) and battleNodeTotal:
                        if (eliteBattleTotal and random() >= 0.5) or (battleNodeTotal == 1 and eliteBattleTotal == 1):
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                Node(3, 0, 0, nodeType = NodeType.SHOP, isZoneEnd=True),
                Node(3, 1, 0, nodeType = NodeType.SHOP, isZoneEnd=True)
            ]
            )
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
            
        case 2:
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            scout_gen = True
            passage_gen = True
            new_map = Map(zone, index)
            eliteBattleTotal = choice([0,1])
            if random() >= 0.65:
                total_node = 6
            else:
                total_node = 5
            mapMode = randomizePutNode(total_node, 2 ,[[2,3],[2,3]])
            for i in range(total_node):
                if random() <= 0.6:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.15 and safe_house_gen:
                    nonBattlePool.append(choice([NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.10 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.2 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.1 and shop_gen:
                    nonBattlePool.append(choice([NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.2 and lost_and_found_gen:
                    nonBattlePool.append(choice([NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if scout_gen:
                    nonBattlePool.append(choice([NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 1, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER]))
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0.5
                if i[0].x == 2:
                    random_chance = 0.6
                for j in i:
                    if (random() <= random_chance or (not nonBattlePool)) and battleNodeTotal:
                        if eliteBattleTotal and random() >= 0.5:
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                Node(3, 0, 0, nodeType = NodeType.WISH, isZoneEnd=True),
                Node(3, 1, 0, nodeType = NodeType.WISH, isZoneEnd=True)
            ]
            )
            
            
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
            
            
        case 3:
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            scout_gen = True
            passage_gen = True
            rd = random()
            new_map = Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.02:
                total_node = 9
            elif rd <= 0.2:
                total_node = 10
            elif rd <= 0.8:
                total_node = 11
            else:
                total_node = 12
            mapMode = randomizePutNode(total_node, 3 ,[[3,4],[3,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.35 and safe_house_gen:
                    nonBattlePool.append(choice([NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.30 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.25 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.50 and shop_gen:
                    nonBattlePool.append(choice([NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if lost_and_found_gen:
                    nonBattlePool.append(choice([NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if random() <= 0.50 and scout_gen:
                    nonBattlePool.append(choice([NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 1, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 2, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER]))
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0.33
                if i[0].x == 2:
                    random_chance = 0.33
                if i[0].x == 3:
                    random_chance = 0.33
                for j in i:
                    if (random() <= random_chance or (not nonBattlePool)) and battleNodeTotal:
                        if eliteBattleTotal and random() >= 0.5:
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                Node(4, 0, 0, nodeType = NodeType.BOSS, stage = choice(ZONE_3_ELITE_BOSS_POOL) if alternativeBoss else choice(ZONE_3_NORMAL_BOSS_POOL), isZoneEnd=True)
            ]
            )
            
            
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        
        case 4 | 114514:
            if zone == 114514:
                zone = 1
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            scout_gen = True
            passage_gen = True
            passage_gen_2 = True
            rd = random()
            new_map = Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.02:
                total_node = 9
            elif rd <= 0.5:
                total_node = 10
            else:
                total_node = 11
            mapMode = randomizePutNode(total_node, 3 ,[[2,4],[2,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.6:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.40 and safe_house_gen:
                    nonBattlePool.append(choice([NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.30 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.10 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.35 and shop_gen:
                    nonBattlePool.append(choice([NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.50 and lost_and_found_gen:
                    nonBattlePool.append(choice([NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if scout_gen:
                    nonBattlePool.append(choice([NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                if random() <= 0.25 and passage_gen_2:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen_2 = False
                    continue
                passage_gen_2 = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 1, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 2, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER]))
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0.2
                if i[0].x == 2:
                    random_chance = 0.3
                if i[0].x == 3:
                    random_chance = 0.5
                for j in i:
                    if (random() <= random_chance or (not nonBattlePool)) and battleNodeTotal:
                        if eliteBattleTotal and random() >= 0.5:
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                Node(4, 0, 0, nodeType = NodeType.WISH, isZoneEnd=True),
                Node(4, 1, 0, nodeType = NodeType.WISH, isZoneEnd=True),
                Node(4, 2, 0, nodeType = NodeType.WISH, isZoneEnd=True)]
            )
            
            
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        
        case 5:
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            passage_gen = True
            passage_gen_2 = True
            rd = random()
            new_map = Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.1:
                total_node = 9
            elif rd <= 0.4:
                total_node = 10
            elif rd <= 0.8:
                total_node = 11
            else:
                total_node = 12
            mapMode = randomizePutNode(total_node, 3 ,[[2,4],[2,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.6 and safe_house_gen:
                    nonBattlePool.append(choice([NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.6 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.25 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.50 and shop_gen:
                    nonBattlePool.append(choice([NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if lost_and_found_gen:
                    nonBattlePool.append(choice([NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                if random() <= 0.25 and passage_gen_2:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen_2 = False
                    continue
                passage_gen_2 = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 1, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER])),
                    Node(0, 2, 0, nodeType = choice([NodeType.NORMAL_BATTLE, NodeType.ENCOUNTER]))
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0.33
                if i[0].x == 2:
                    random_chance = 0.33
                if i[0].x == 3:
                    random_chance = 0.33
                for j in i:
                    if (random() <= random_chance or (not nonBattlePool)) and battleNodeTotal:
                        if eliteBattleTotal and random() >= 0.5:
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append(
                [
                    Node(4, x, 0, nodeType = NodeType.STORY) for x in range(choice([1,2,2,3,3,3,3,4,4,4,4,4,4,4,4]))
                ]
            )
            nodeList.append([
                Node(5, 0, 0, nodeType = NodeType.BOSS, stage = "ro3_b_4_b" if alternativeBoss else "ro3_b_4", isZoneEnd=True)]
            )
            
            
            generateRoute(nodeList, True)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        
        
        case 6:   
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            passage_gen = True
            passage_gen_2 = True
            rd = random()
            new_map = Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.3:
                total_node = 3
            else:
                total_node = 4
            mapMode = randomizePutNode(total_node, 2 ,[[1,2],[1,2]])
            for i in range(mapMode[1]):
                battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.3 and safe_house_gen:
                    nonBattlePool.append(choice([NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.25 and entertainment_gen:
                    nonBattlePool.append(choice([NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.2 and wish_gen:
                    nonBattlePool.append(choice([NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.3 and shop_gen:
                    nonBattlePool.append(choice([NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    Node(0, 0, 0, nodeType = NodeType.SHOP)
                ]
            ]
            
            for i in tmpNodeList:
                if i[0].x == 1:
                    random_chance = 0
                if i[0].x == 2:
                    random_chance = 1
                for j in i:
                    if (random() < random_chance) and battleNodeTotal:
                        if eliteBattleTotal and random() >= 0.3:
                            j.setNodeType(NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    else:
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                Node(3, 0, 0, nodeType = NodeType.BOSS, stage = "ro3_b_6_b" if alternativeBoss else "ro3_b_6", isZoneEnd=True)]
            )
            
            
            generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        """

def generateSightByVision(zone: int, currentPosition: dict | None, vision: int, mapData: dict) -> dict:
    if not currentPosition:
        position = {
            "x": -1,
            "y": 0
        }
    else:
        position = currentPosition
        
    currentNode = mapData[str(zone)]["nodes"][f"{position["x"]}0{position["y"]}" if position["x"] != 0 else f"{position["y"]}"] if position["x"] != -1 else None
    nextNode = [mapData[str(zone)]["nodes"][f"{node["x"]}0{node["y"]}"] \
            for node in currentNode["next"]]  if position["x"] != -1 else [mapData[str(zone)]["nodes"][f"{node["pos"]["y"]}"] \
            for node in mapData[str(zone)]["nodes"].values() if node["pos"]["x"] == 0]
    
    match vision:
        case 0:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                    print(1)
                    #node["realNodeType"] = node["type"]
                    node["type"] = NodeType.UNKNOWN
                    node["visibility"] = 2
                elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                    #node["realNodeType"] = node["type"]
                    node["type"] = NodeType.UNKNOWN
                    node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 1 | 2:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["pos"]["x"] > position["x"] + 1:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 3:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["pos"]["x"] > position["x"] + 2:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case 4 | 5:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["pos"]["x"] > position["x"] + 3:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
        case vision if vision >= 6:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["pos"]["x"] > position["x"] + 99999:
                    if node["realNodeType"] == NodeType.ELITE_BATTLE or node["realNodeType"] == NodeType.NORMAL_BATTLE:
                        #node["realNodeType"] = node["type"]
                        node["type"]= NodeType.UNKNOWN
                        node["visibility"]= 2
                    elif node["realNodeType"] != NodeType.BOSS and node["realNodeType"] != NodeType.STORY and node["visibility"] != 2:   #todo：路网额外紧急能见度判定
                        #node["realNodeType"] = node["type"]
                        node["type"] = NodeType.UNKNOWN
                        node["visibility"] = 1
                else:
                    node["type"] = node["realNodeType"]
                    node["visibility"] = 0
                    
    for node in nextNode:
        node["type"] = node["realNodeType"]
    if currentNode:
        currentNode["visibility"] = 0
        currentNode["type"] = currentNode["realNodeType"]
                
    
        
    return mapData
