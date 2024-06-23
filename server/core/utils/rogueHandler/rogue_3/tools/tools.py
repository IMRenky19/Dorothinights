from server.core.database.function.userData import getAccountBySecret
from .....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import shuffle, randint, sample
from copy import deepcopy
from server.core.utils.json import read_json


ts = time()
def createGameBase():
        initial = {
        "player": {
            "state": "INIT",
            "property": {
                "exp": 0,
                "level": 1,
                "maxLevel": 10,
                "hp": {
                    "current": 8,
                    "max": 8
                },
                "gold": 6,
                "shield": 0,
                "capacity": 6,
                "population": {
                    "cost": 0,
                    "max": 6
                },
                "conPerfectBattle": 0
            },
            "cursor": {
                "zone": 0,
                "position": None
            },
            "trace": [],
            "pending": [
                {
                    "index": "e_0",
                    "type": "GAME_INIT_RELIC",
                    "content": {
                        "initRelic": {
                            "step": [
                                1,
                                3
                            ],
                            "items": {}
                        }
                    }
                },
                {
                    "index": "e_1",
                    "type": "GAME_INIT_RECRUIT_SET",
                    "content": {
                        "initRecruitSet": {
                            "step": [
                                2,
                                3
                            ],
                            "option": {}
                        }
                    }
                },
                {
                    "index": "e_2",
                    "type": "GAME_INIT_RECRUIT",
                    "content": {
                        "initRecruit": {
                            "step": [
                                3,
                                3
                            ],
                            "tickets": [],
                            "showChar": [],
                            "team": None
                        }
                    }
                }
            ],
            "status": {
                "bankPut": 0
            },
            "toEnding": None,
            "chgEnding": False
        },
        "record": {
            "brief": None
        },
        "map": {
            "zones": {}
        },
        "troop": {
            "chars": {},
            "expedition": [],
            "expeditionReturn": None,
            "hasExpeditionReturn": False
        },
        "inventory": {
            "relic": {},
            "recruit": {},
            "trap": None,
            "consumable": {},
            "exploreTool": {}
        },
        "game": {
            "mode": None,
            "predefined": None,
            "theme": None,
            "outer": {
                "support": False
            },
            "start": ts,
            "modeGrade": None,
            "equivalentGrade": None
        },
        "buff": {
            "tmpHP": 0,
            "capsule": None,
            "squadBuff": []
        },
        "module":{}
    }
        return initial


def getOutBuffs(rogueClass: RogueBasicModel):
        rlv2_tmp = rogueClass.rlv2
        outer_buff = rlv2_tmp["outer"]["rogue_3"]["buff"]
        ex_buff_outer = {
            "extra_atk": 0,
            "extra_gold": 0,
            "extra_def": 0,
            "extra_hp": 0,
            "extra_exp": 0,
            "extra_capacity": 0,             #携带位
            "extra_char_limit": 0,           #部署位
            "extra_hp_limit": 0,
            "extra_grow_point": 0,           #生态标本，暂不使用
            "add_hp_limit_hp": 0,            #生命值不高于这个数值每完美作战一次**可选择**回复1血，0禁用
            "lost_and_found_enable": 0,      #是否生成失与得，0禁用，下同
            "scout_enable": 0,               #是否生成先行一步
            "passage_enable": 0,             #是否生成树篱之途
            "refresh_shop": 0,               #是否可刷新商店
            "more_totem": 0,                 #是否额外掉落一个密文版
            "3_add_vision": 0,               #3层是否+1抗
            "band_11_unlock": 0,             #永恒狩猎分队
            "band_12_unlock": 0,             #生活至上分队
            "band_13_unlock": 0,             #科学主义分队
            "difficulty_1_buff": 0,          #3级及以上buff(仅判定解锁状态)
            "difficulty_2_buff": 0,          #6级及以上buff
            "difficulty_3_buff": 0,          #9级及以上buff
            "seed": randint(-1000000000000,1000000000000)
        }
        
        for buff, status in outer_buff["unlocked"].items():
            if status == 1:
                match buff:
                    case "rogue_3_outbuff_1":
                        ex_buff_outer["extra_hp"] += 0.03
                    case "rogue_3_outbuff_2":
                        ex_buff_outer["extra_atk"] += 0.03
                    case "rogue_3_outbuff_3":
                        ex_buff_outer["extra_grow_point"] += 0.05
                    case "rogue_3_outbuff_4":
                        ex_buff_outer["extra_def"] += 0.03
                    case "rogue_3_outbuff_5":
                        ex_buff_outer["lost_and_found_enable"] = 1
                    case "rogue_3_outbuff_6":
                        ex_buff_outer["passage_enable"] = 1
                    case "rogue_3_outbuff_7":
                        ex_buff_outer["scout_enable"] = 1
                    case "rogue_3_difficulty_1":
                        ex_buff_outer["difficulty_1_buff"] = 1
                    case "rogue_3_outbuff_9":
                        ex_buff_outer["extra_def"] += 0.03
                    case "rogue_3_outbuff_10":
                        ex_buff_outer["extra_hp_limit"] += 1
                    case "rogue_3_outbuff_11":
                        ex_buff_outer["extra_char_limit"] += 1
                    case "rogue_3_outbuff_12":
                        ex_buff_outer["extra_hp"] += 0.03
                    case "rogue_3_outbuff_13":
                        ex_buff_outer["extra_gold"] += 4
                    case "rogue_3_outbuff_14":
                        ex_buff_outer["extra_grow_point"] += 0.05
                    case "rogue_3_outbuff_15":
                        ex_buff_outer["extra_atk"] += 0.03
                    case "rogue_3_outbuff_16":
                        ex_buff_outer["add_hp_limit_hp"] = 1
                    case "rogue_3_outbuff_17":
                        ex_buff_outer["extra_exp"] += 0.1
                    case "rogue_3_outbuff_18":
                        ex_buff_outer["extra_grow_point"] += 0.05
                    case "rogue_3_outbuff_19":
                        ex_buff_outer["refresh_shop"] = 1
                    case "rogue_3_outbuff_20":
                        ex_buff_outer["more_totem"] = 1
                    case "rogue_3_outbuff_21":
                        ex_buff_outer["3_add_vision"] = 1
                    case "rogue_3_difficulty_2":
                        ex_buff_outer["difficulty_2_buff"] = 1
                    case "rogue_3_outbuff_23":
                        ex_buff_outer["add_hp_limit_hp"] = 2
                    case "rogue_3_outbuff_24":
                        ex_buff_outer["extra_hp_limit"] += 1
                    case "rogue_3_outbuff_25":
                        ex_buff_outer["extra_capacity"] += 1
                    case "rogue_3_outbuff_26":
                        ex_buff_outer["extra_hp"] += 0.04
                    case "rogue_3_outbuff_27":
                        ex_buff_outer["extra_atk"] += 0.04
                    case "rogue_3_outbuff_28":
                        ex_buff_outer["extra_def"] += 0.04
                    case "rogue_3_outbuff_29":
                        ex_buff_outer["extra_atk"] += 0.04
                    case "rogue_3_outbuff_30":
                        ex_buff_outer["extra_def"] += 0.04
                    case "rogue_3_outbuff_31":
                        ex_buff_outer["extra_exp"] += 0.1
                    case "rogue_3_outbuff_32":
                        ex_buff_outer["extra_hp"] += 0.04
                    case "rogue_3_outbuff_33":
                        ex_buff_outer["band_12_unlock"] = 1
                    case "rogue_3_outbuff_34":
                        ex_buff_outer["band_11_unlock"] = 1
                    case "rogue_3_outbuff_35":
                        ex_buff_outer["band_13_unlock"] = 1
                    case "rogue_3_difficulty_3":
                        ex_buff_outer["difficulty_3_buff"] = 1
                    case "rogue_3_outbuff_37":
                        ex_buff_outer["extra_hp"] += 0.06
                    case "rogue_3_outbuff_38":
                        ex_buff_outer["extra_gold"] += 4
                    case "rogue_3_outbuff_39":
                        ex_buff_outer["extra_grow_point"] += 0.05
                    case "rogue_3_outbuff_40":
                        ex_buff_outer["add_hp_limit_hp"] = 3
                    case "rogue_3_outbuff_41":
                        ex_buff_outer["extra_exp"] += 0.1
                    case "rogue_3_outbuff_42":
                        ex_buff_outer["extra_def"] += 0.06
                    case "rogue_3_outbuff_43":
                        ex_buff_outer["extra_atk"] += 0.06
        
        ex_buff_outer["extra_exp"] = round(ex_buff_outer["extra_exp"], 2)
        rogueClass.extension.update(ex_buff_outer)
        
        
        
def getInnerBuffs(rogueClass: RogueBasicModel, hardLevel: int):
        ex_buff_inner = {
            "hardLevel": hardLevel,
            "1_chaos_deeper": 0,             #1级buff：坍缩值12以上时坍缩值更容易加深
            "3_more_chaos": 0,               #3级buff：非完美作战额外增加1点坍缩值
            "stronger_relics": 0,            #3, 6, 9级buff：多元奇物展现出高寒/冻土/极地化效果(0禁用，1高寒，2冻土，3极地)
            "6_more_population": 0,          #6级buff：招募4星及以干员时希望消耗+1
            "12_less_vision": 0,             #12级buff：进入第一、三、五层时抗干扰指数-1
            "12_alter_boss": 0,              #（DLC2内容）12级buff：有概率出现不同的险路恶敌战斗
            "15_more_chaos": 0,              #15级buff：进入新层增长的坍缩值递增1点
            "scout_bring_gold": 0,           #文化比较N6buff：“先行一步”节点派遣的队员可带来2-5源石锭
            "more_goods": 0,                 #文化比较N6buff：诡意行商中会额外出售两个商品
            "safe_house_add_hp": 0,          #文化比较N9buff：进入“安全的角落”节点回复1目标生命
            "add_shield": 0,                 #文化比较N9buff：目标生命高于10时，完美作战后获得1护盾值
            "difficulty_multiplier": 0,      #敌人数值乘区
            "score_multiplier": 1,           #分数乘区
            "band_direct_upgrade":0,         #职业队直升，0禁用，1近锋，2重辅，3狙医，4术特
            "no_upgrade_population":0,       #升级是否不消耗希望
            "totem_modify": 0,               #密文修饰概率
            "band_13_another_vision_set": 0  #科学主义分队效果：每层+2抗干扰
            
        }
        
        #1,2,3,6,9,12,15
        if hardLevel >= 1:
            ex_buff_inner["1_chaos_deeper"] = 1
            if hardLevel >= 2:
                rogueClass.extension["extra_hp_limit"] -= 4
                if hardLevel >= 3:
                    ex_buff_inner["stronger_relics"] = 1
                    if rogueClass.extension["difficulty_1_buff"]:
                        rogueClass.extension["extra_hp"] += 0.03
                        rogueClass.extension["extra_exp"] += 0.05
                        rogueClass.extension["extra_gold"] += 2
                    if hardLevel >= 6:
                        ex_buff_inner["stronger_relics"] = 2
                        ex_buff_inner["6_more_population"] = 1
                        if rogueClass.extension["difficulty_2_buff"]:
                            rogueClass.extension["extra_atk"] += 0.03
                            ex_buff_inner["scout_bring_gold"] = 1
                            ex_buff_inner["more_goods"] = 1
                        if hardLevel >= 9:
                            rogueClass.extension["extra_char_limit"] -= 1
                            ex_buff_inner["stronger_relics"] = 3
                            if rogueClass.extension["difficulty_2_buff"]:
                                rogueClass.extension["extra_def"] += 0.03
                                ex_buff_inner["safe_house_add_hp"] = 1
                                ex_buff_inner["add_shield"] = 1
                            if hardLevel >= 12:
                                ex_buff_inner["12_less_vision"] = 1
                                ex_buff_inner["12_alter_boss"] = 1
                                if hardLevel >= 15:
                                    ex_buff_inner["15_more_chaos"] = 1
        
        match hardLevel:
            case 0:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0, 0.6, 0]
            case 1:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0, 0.8, 0]
            case 2:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0, 1, 0]
            case 3:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0, 1.1, 0.05]
            case 4:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0, 1.2, 0.075]
            case 5:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.01, 1.25, 0.1]
            case 6:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.02, 1.3, 0.125]
            case 7:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.03, 1.35, 0.15]
            case 8:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.04, 1.4, 0.175]
            case 9:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.05, 1.45, 0.2]
            case 10:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.06, 1.5, 0.2]
            case 11:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.08, 1.5, 0.2]
            case 12:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.1, 1.5, 0.2]
            case 13:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.12, 1.5, 0.2]
            case 14:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.14, 1.5, 0.2]
            case 15:
                ex_buff_inner["difficulty_multiplier"], ex_buff_inner["score_multiplier"], ex_buff_inner["totem_modify"] = [0.16, 1.5, 0.2]
                
        rogueClass.extension.update(ex_buff_inner)
          
def getRogueData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.rlv2)

def getRogueExtensionData(rogueClass: RogueBasicModel) -> dict:
    return deepcopy(rogueClass.extension)
          
  
def addHpLimit(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] += add
    rlv2_data["current"]["player"]["property"]["hp"]["max"] += add
    
def setHpLimit(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["hp"]["max"] = sets
    
def setHp(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] = sets
    
def addHp(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["hp"]["current"] += add
    
def setShield(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["shield"] = sets
    
def addShield(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["shield"] += add
    
def setGold(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["gold"] = sets
    
def addGold(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["gold"] += add
    
def addCharLimit(extension: dict, add: int):
    extension["extra_char_limit"] += add
    
def setPopulation(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["population"]["max"] = sets
    
def addPopulation(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["population"]["max"] += add
    
def setCapacity(rlv2_data: dict, sets: int):
    rlv2_data["current"]["player"]["property"]["capacity"] = sets
    
def addCapacity(rlv2_data: dict, add: int):
    rlv2_data["current"]["player"]["property"]["capacity"] += add
    
def getCurrentState(rlv2_data: dict):
    return rlv2_data["current"]["player"]["state"]

def setCurrentState(rlv2_data: dict, sets: str):
    rlv2_data["current"]["player"]["state"] = sets
    
def setPending(rlv2_data: dict, pending: list):
    rlv2["player"]["pending"] = pending
    
def setVision(rlv2_data: dict, sets: int):
    rlv2_data["current"]["module"]["vision"]["value"] = sets
    
def addVision(rlv2_data: dict, add: int):
    rlv2_data["current"]["module"]["vision"]["value"] += add
    

def getBand(rlv2_data: dict):
    return rlv2_data["current"]['inventory']['relic']['r_0']['id']

def getNextTicketIndex(rlv2_data: dict):
    d = set()
    for e in rlv2_data["current"]["inventory"]["recruit"]:
        d.add(int(e[2:]))
    i = 0
    while i in d:
        i += 1
    return f"t_{i}"

def getNextPendingIndex(rlv2_data: dict):
    d = set()
    for e in rlv2_data["current"]["player"]["pending"]:
        d.add(int(e["index"][2:]))
    i = 0
    while i in d:
        i += 1
    return f"e_{i}"

def getNextCharId(rlv2):
    i = 0
    while str(i) in rlv2["current"]["troop"]["chars"]:
        i += 1
    return str(i)

def getNextZoneId(rlv2):
    i = 1
    while str(i) in rlv2["current"]["map"]["zones"].keys():
        i += 1
    return int(i)


def addTicket(rlv2_data: dict, ticket_id: str, init: bool, profession: str = 'all'):
    theme = rlv2_data["game"]["theme"]
    theme_id = theme.split('_')[-1]
    ticket = f"rogue_{theme_id}_recruit_ticket_{profession}"
    rlv2_data["inventory"]["recruit"][ticket_id] = {
        "index": ticket_id,
        "id": ticket,
        "state": 0,
        "list": [],
        "result": None,
        "ts": ts,
        "from": "initial",
        "mustExtra": 0,
        "needAssist": init
    }
    rlv2_data["player"]["pending"][0]["content"]["initRecruit"]["tickets"].append(
        ticket_id
    )
    
    
async def getChars(rlv2_data: RogueBasicModel, professions: list, secret: str):
    extra_recruit = 0
    extra_upgrade = 0
    direct_upgrade: int = rlv2_data.extension["band_direct_upgrade"]
    no_upgrade_population: int = rlv2_data.extension["no_upgrade_population"]
    user = await getAccountBySecret(secret)
    is_n6 = rlv2_data.extension["6_more_population"]
    
    rarity4, rarity5, rarity6, chars_upgrade, chars_new, chars_2 = [],[],[],[],[],[]
    for profession in professions:
        profession_direct_upgrade=0
        if (profession in ["warrior","pioneer"] and direct_upgrade == 1) \
        or (profession in ["tank","support"] and direct_upgrade == 2) \
        or (profession in ["sniper","medic"] and direct_upgrade == 3) \
        or (profession in ["caster","special"] and direct_upgrade == 4):
            profession_direct_upgrade=True
            extra_recruit -= 2
            extra_upgrade -= 1
        if no_upgrade_population == 1:
            free_upgrade = True
        user_data = user.user
        
        chars = [
            user_data["troop"]["chars"][i] for i in user_data["troop"]["chars"]
        ]
        if is_n6:
            extra_recruit += 1
        else:
            extra_recruit += 0

        for char in chars:
            clone_man = False
            if char["charId"] in ["char_504_rguard","char_514_rdfend","char_505_rcast","char_506_rmedic","char_507_rsnipe"]:
                clone_man = True

            if char["profession"] != profession.upper():
                if (profession in ["warrior","pioneer","special"] and char["charId"] == "char_504_rguard") \
                or (profession in ["tank"] and char["charId"] == "char_514_rdfend") \
                or (profession in ["support","caster"] and char["charId"] == "char_505_rcast") \
                or (profession in ["medic"] and char["charId"] == "char_506_rmedic") \
                or (profession in ["sniper"] and char["charId"] == "char_507_rsnipe"):
                    clone_man = True
                else:    
                    continue
            if int(char["rarity"]) < 4:
                rarity = 0
            elif int(char["rarity"]) == 4:
                rarity = 2 + extra_recruit
            elif int(char["rarity"]) == 5:
                rarity = 3 + extra_recruit
            elif int(char["rarity"]) == 6:
                rarity = 6 + extra_recruit
            if clone_man:
                current_type = "THIRD_LOW"
            else:
                current_type = "NORMAL"
            char.update(
                {
                    "type": current_type,
                    "upgradeLimited": False,
                    "upgradePhase": 1,
                    "isUpgrade": False,
                    "isCure": False,
                    "population": rarity,
                    "charBuff": [],
                    "troopInstId": "0"
                }
            )
            chars_2.append(char)
            if int(char["rarity"]) == 4:
                rarity4.append(char)
            if int(char["rarity"]) == 5:
                rarity5.append(char)
            if int(char["rarity"]) == 6:
                rarity6.append(char)
        chars = deepcopy(chars_2)
        if profession_direct_upgrade:
            upgrade4 = sample(rarity4, 2)
            upgrade5 = sample(rarity5, 3)
            upgrade6 = sample(rarity6, 6)
            for i in upgrade4:
                rand = randint(1,100)
                if rand <= 80:
                    chars.remove(i)
                    i.update({"type": "UPGRADE_BONUS"})
                    chars_upgrade.append(i)
            for i in upgrade5:
                rand = randint(1,100)
                if rand <= 80:
                    chars.remove(i)
                    i.update({"type": "UPGRADE_BONUS"})
                    chars_upgrade.append(i)
            rand = randint(1,100)
            if rand <= 35:
                for i in upgrade6:
                    chars.remove(i)
                    i.update({"type": "UPGRADE_BONUS"})
                    chars_upgrade.append(i)
        """if current_population < 7:            
            for char in chars:
                if char["population"] >= current_population:
                    chars.insert(0,char)
                    chars.remove(char)"""

        """
        1,降级（new list）
        2，直升（同）
        3，1-2步list拼合，排序（可抓在前）
        4，加instid
        5，输出



        """
        for i in range(len(chars)):
            char = chars[i]
            if char["evolvePhase"] == 2:
                char_alt = deepcopy(char)
                char_alt["evolvePhase"] = 1
                match int(len(char_alt["skills"])):
                    case 0:
                        tmp_level = 55
                    case 1:
                        tmp_level = 60
                    case 2:
                        tmp_level = 70
                    case 3:
                        tmp_level = 80
                char_alt["level"] = tmp_level
                if len(char_alt["skills"]) == 3:
                    char_alt["defaultSkillIndex"] = 1
                    char_alt["skills"][-1]["unlock"] = 0
                for skill in char_alt["skills"]:
                    skill["specializeLevel"] = 0
                char_alt["currentEquip"] = None

                #阿米娅暂缓
                """if char["charId"] == "char_002_amiya":
                    tmpls = list(char_alt["tmpl"].keys())
                    print(tmpls)
                    for j in tmpls:
                        if len(char_alt["tmpl"][j]["skills"]) == 3:
                            char_alt["tmpl"][j]["defaultSkillIndex"] = 1
                            char_alt["tmpl"][j]["skills"][-1]["unlock"] = 0
                        for skill in char_alt["tmpl"][j]["skills"]:
                            skill["specializeLevel"] = 0
                        char_alt["tmpl"][j]["currentEquip"] = None
                    char["currentTmpl"] = tmpls[0]
                    char_alt["currentTmpl"] = tmpls[0]
                    for j in range(0, len(tmpls)):
                        for k in [char, char_alt]:
                            char_alt_alt = deepcopy(k)
                            if char_alt_alt["evolvePhase"] == 2:
                                continue
                            char_alt_alt["currentTmpl"] = tmpls[j]
                            chars_new.append(char_alt_alt)
                            #print(char_alt_alt)
                    continue"""

                chars_new.append(char_alt)
            else:
                chars_new.append(char)
    for i in chars_new:
        chars_new.remove(i)
        i.update({"type": "NORMAL"})
        chars_new.append(i)
    chars_final = chars_new + chars_upgrade
    for i in range(len(chars_final)):
        if chars_final[i]["evolvePhase"] < 2:
            chars_final[i]["upgradeLimited"] = True
            chars_final[i]["upgradePhase"] = 0
        chars_final[i].update({"instId": str(i)})
    return chars_final
    
    
