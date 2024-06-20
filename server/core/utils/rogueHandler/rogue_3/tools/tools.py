from .....Model.RogueBase import RogueBasicModel
from server.core.utils.time import time
from random import shuffle, randint


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
            "totem_modify": 0                #密文修饰概率
            
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
            

    