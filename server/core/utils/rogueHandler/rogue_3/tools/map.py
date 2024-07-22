from server.constants import ROGUELIKE_TOPIC_EXCEL_PATH, ROGUE_ROUTE_PATH
from random import shuffle, randint, sample, random, choice
from server.core.utils.json import read_json

from ... import common
from ...common.map import *
route_info: dict = read_json(ROGUE_ROUTE_PATH)

ZONE_3_NORMAL_BOSS_POOL = [
    "ro3_b_1",            #利刃所指
    "ro3_b_2",            #新部族
    "ro3_b_3"             #自然之怒
]

ZONE_3_ELITE_BOSS_POOL = [
    "ro3_b_1_b",            #呼吸
    "ro3_b_2_b",            #夺树者
    "ro3_b_3_b"             #大地醒转
]
      
def mapGenerator(zone: int, index: int, alternativeBoss: bool = False, end_3: bool = False, \
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
            new_map = common.Map(zone, index)
            eliteBattleTotal = 1
            if random() >= 0.55:
                total_node = 6
            else:
                total_node = 5
            mapMode = common.randomizePutNode(total_node, 2 ,[[2,3],[2,3]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.15 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.02 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = common.NodeType.NORMAL_BATTLE),
                    common.Node(0, 1, 0, nodeType = common.NodeType.NORMAL_BATTLE)
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                common.Node(3, 0, 0, nodeType = common.NodeType.SHOP, isZoneEnd=True),
                common.Node(3, 1, 0, nodeType = common.NodeType.SHOP, isZoneEnd=True)
            ]
            )
            common.generateRoute(nodeList)
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
            new_map = common.Map(zone, index)
            eliteBattleTotal = choice([0,1])
            if random() >= 0.65:
                total_node = 6
            else:
                total_node = 5
            mapMode = common.randomizePutNode(total_node, 2 ,[[2,3],[2,3]])
            for i in range(total_node):
                if random() <= 0.6:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.15 and safe_house_gen:
                    nonBattlePool.append(choice([common.NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.10 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.2 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.1 and shop_gen:
                    nonBattlePool.append(choice([common.NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.2 and lost_and_found_gen:
                    nonBattlePool.append(choice([common.NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if scout_gen:
                    nonBattlePool.append(choice([common.NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 1, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER]))
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                common.Node(3, 0, 0, nodeType = common.NodeType.WISH, isZoneEnd=True),
                common.Node(3, 1, 0, nodeType = common.NodeType.WISH, isZoneEnd=True)
            ]
            )
            
            
            common.generateRoute(nodeList)
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
            new_map = common.Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.02:
                total_node = 9
            elif rd <= 0.2:
                total_node = 10
            elif rd <= 0.8:
                total_node = 11
            else:
                total_node = 12
            mapMode = common.randomizePutNode(total_node, 3 ,[[3,4],[3,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.35 and safe_house_gen:
                    nonBattlePool.append(choice([common.NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.30 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.25 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.50 and shop_gen:
                    nonBattlePool.append(choice([common.NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if lost_and_found_gen:
                    nonBattlePool.append(choice([common.NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if random() <= 0.50 and scout_gen:
                    nonBattlePool.append(choice([common.NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 1, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 2, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER]))
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                common.Node(4, 0, 0, nodeType = common.NodeType.BOSS, stage = choice(ZONE_3_ELITE_BOSS_POOL) if alternativeBoss else choice(ZONE_3_NORMAL_BOSS_POOL), isZoneEnd=True)
            ]
            )
            
            
            common.generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        
        case 4:
            safe_house_gen = True
            entertainment_gen = True
            wish_gen = True
            shop_gen = True
            lost_and_found_gen = True
            scout_gen = True
            passage_gen = True
            passage_gen_2 = True
            rd = random()
            new_map = common.Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.02:
                total_node = 9
            elif rd <= 0.5:
                total_node = 10
            else:
                total_node = 11
            mapMode = common.randomizePutNode(total_node, 3 ,[[2,4],[2,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.6:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.40 and safe_house_gen:
                    nonBattlePool.append(choice([common.NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.30 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.10 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.35 and shop_gen:
                    nonBattlePool.append(choice([common.NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.50 and lost_and_found_gen:
                    nonBattlePool.append(choice([common.NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if scout_gen:
                    nonBattlePool.append(choice([common.NodeType.SCOUT]))
                    scout_gen = False
                    continue
                scout_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                if random() <= 0.25 and passage_gen_2:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen_2 = False
                    continue
                passage_gen_2 = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 1, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 2, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER]))
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                common.Node(4, 0, 0, nodeType = common.NodeType.WISH, isZoneEnd=True),
                common.Node(4, 1, 0, nodeType = common.NodeType.WISH, isZoneEnd=True),
                common.Node(4, 2, 0, nodeType = common.NodeType.WISH, isZoneEnd=True)]
            )
            
            
            common.generateRoute(nodeList)
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
            new_map = common.Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.1:
                total_node = 9
            elif rd <= 0.4:
                total_node = 10
            elif rd <= 0.8:
                total_node = 11
            else:
                total_node = 12
            mapMode = common.randomizePutNode(total_node, 3 ,[[2,4],[2,4],[2,4]])
            for i in range(total_node):
                if random() <= 0.5:
                    battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.6 and safe_house_gen:
                    nonBattlePool.append(choice([common.NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.6 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.25 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.50 and shop_gen:
                    nonBattlePool.append(choice([common.NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if lost_and_found_gen:
                    nonBattlePool.append(choice([common.NodeType.LOST_AND_FOUND]))
                    lost_and_found_gen = False
                    continue
                lost_and_found_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                if random() <= 0.25 and passage_gen_2:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen_2 = False
                    continue
                passage_gen_2 = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 1, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER])),
                    common.Node(0, 2, 0, nodeType = choice([common.NodeType.NORMAL_BATTLE, common.NodeType.ENCOUNTER]))
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    if nonBattlePool or (not battleNodeTotal):
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append(
                [
                    common.Node(4, x, 0, nodeType = common.NodeType.STORY) for x in range(choice([1,2,2,3,3,3,3,4,4,4,4,4,4,4,4]))
                ]
            )
            nodeList.append([
                common.Node(5, 0, 0, nodeType = common.NodeType.BOSS, stage = "ro3_b_4_b" if alternativeBoss else "ro3_b_4", isZoneEnd=True)]
            )
            
            
            common.generateRoute(nodeList, True)
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
            new_map = common.Map(zone, index)
            eliteBattleTotal = choice([0,1,2])
            if rd <= 0.3:
                total_node = 3
            else:
                total_node = 4
            mapMode = common.randomizePutNode(total_node, 2 ,[[1,2],[1,2]])
            for i in range(mapMode[1]):
                battleNodeTotal += 1
            for i in range(total_node - battleNodeTotal):
                if random() <= 0.3 and safe_house_gen:
                    nonBattlePool.append(choice([common.NodeType.SAFE_HOUSE]))
                    safe_house_gen = False
                    continue
                safe_house_gen = False
                if random() <= 0.25 and entertainment_gen:
                    nonBattlePool.append(choice([common.NodeType.ENTERTAINMENT]))
                    entertainment_gen = False
                    continue
                entertainment_gen = False
                if random() <= 0.2 and wish_gen:
                    nonBattlePool.append(choice([common.NodeType.WISH]))
                    wish_gen = False
                    continue
                wish_gen = False
                if random() <= 0.3 and shop_gen:
                    nonBattlePool.append(choice([common.NodeType.SHOP]))
                    shop_gen = False
                    continue
                shop_gen = False
                if random() <= 0.25 and passage_gen:
                    nonBattlePool.append(choice([common.NodeType.PASSAGE]))
                    passage_gen = False
                    continue
                passage_gen = False
                nonBattlePool.append(choice([common.NodeType.ENCOUNTER]))            #todo
            for i, x_tmp in zip(mapMode, range(len(mapMode))):
                tmpNodeList.append([])
                for y_tmp in range(i):
                    tmpNodeList[x_tmp].append(common.Node(x=x_tmp + 1, y=y_tmp))
            nodeList = [
                [
                    common.Node(0, 0, 0, nodeType = common.NodeType.SHOP)
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
                            j.setNodeType(common.NodeType.ELITE_BATTLE)
                            eliteBattleTotal -= 1
                            battleNodeTotal -= 1
                            continue
                        else:
                            j.setNodeType(common.NodeType.NORMAL_BATTLE)
                            battleNodeTotal -= 1
                            continue
                    
                    else:
                         j.setNodeType(choice([nonBattlePool.pop()]))
            nodeList += tmpNodeList
            nodeList.append([
                common.Node(3, 0, 0, nodeType = common.NodeType.BOSS, stage = "ro3_b_6_b" if alternativeBoss else "ro3_b_6", isZoneEnd=True)]
            )
            
            
            common.generateRoute(nodeList)
            for i in nodeList:
                for j in i:
                    new_map.addNode(j)
            return new_map.exportMap()
        

def visionGenerator(zone: int, currentPosition: dict | None, vision: int, mapData: dict) -> dict:
    return generateSightByVision(zone, currentPosition, vision, mapData)

def positionToIndex(position: dict):
    return f"{position["x"]}0{position["y"]}" if position["x"] != 0 else f"{position["y"]}"

def generateSightByVision(zone: int, currentPosition: dict | None, vision: int, mapData: dict) -> dict:
    if not currentPosition:
        position = {
            "x": -1,
            "y": 0
        }
    else:
        position = currentPosition
        
    currentNode = mapData[str(zone)]["nodes"][positionToIndex(position)] if position["x"] != -1 else None
    nextNode = [mapData[str(zone)]["nodes"][positionToIndex(node)] \
            for node in currentNode["next"]]  if position["x"] != -1 else [mapData[str(zone)]["nodes"][str(node["pos"]["y"])] \
            for node in mapData[str(zone)]["nodes"].values() if node["pos"]["x"] == 0]
    
    match vision:
        case 0:
            for node_position, node in mapData[str(zone)]["nodes"].items():
                if node["pos"]["x"] < position["x"]:
                    continue
                if node["alwaysVisible"]:
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
                if node["alwaysVisible"]:
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
                if node["alwaysVisible"]:
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
                if node["alwaysVisible"]:
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
                if node["alwaysVisible"]:
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
