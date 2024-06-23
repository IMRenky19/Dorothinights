from .time import time
from .json import read_json
from server.constants import STAGE_EXCEL_PATH, STORY_EXCEL_PATH, CHAR_EXCEL_PATH, \
    SKIN_EXCEL_PATH, UNIEQUIP_EXCEL_PATH, HANDBOOK_INFO_EXCEL_PATH, \
        RETRO_EXCEL_PATH, DISPLAY_META_EXCEL_PATH,STORY_REVIEW_EXCEL_PATH, \
            STORY_REVIEW_META_EXCEL_PATH, ENEMY_HANDBOOK_EXCEL_PATH, ACTIVITY_EXCEL_PATH, \
                MEDAL_EXCEL_PATH, RLV2_INITIAL_PATH
from random import randint as rd


def decrypt_user_key(key: str, login_time: int) -> str:

    LOG_SECRET_KEY = "12451c15120f1c1b203d421a3b132ecf"

    buf = [int(x, 16) for x in
           [y.replace("f", "") for y in [LOG_SECRET_KEY[z:z + 2] for z in range(0, len(LOG_SECRET_KEY), 2)]]]
    data_bin = "".join([format(ord(x), '08b') for x in key])
    format_data = [data_bin[i:i + 8] for i in range(0, len(data_bin), 8)]
    try:
        decrypt_buf = "".join(['{:08b}'.format(int(format_data[i], 2) - buf[i]) if i in (6, 15) else '{:08b}'.format(
            int(format_data[i], 2) + buf[i]) for i in range(len(format_data))])
        decrypt_data = "".join(map(lambda x: chr(int(str(x), 2)), [decrypt_buf[i:i + 8] for i in
                                                                   range(0, len(decrypt_buf),
                                                                         8)])) if login_time else None
        return decrypt_data

    except Exception as e:
        return None
    

async def generateNewSyncData(uid: str | int) -> dict:
    ts = time()
    rlv2 = read_json(RLV2_INITIAL_PATH)
    newSyncData = {
        "result": 0,
        "ts": ts,
        "user": {
            "dungeon": {
                "stages": {},
                "cowLevel": {},
                "hideStages": {},
                "mainlineBannedStages": []
            },
            "activity": {},
            "status": {},
            "troop": {},
            "npcAudio": {},
            "pushFlags": {},
            "equipment": {},
            "skin": {},
            "shop": {},
            "mission": {},
            "social": {},
            "building": {},
            "dexNav": {
                "character": {},
                "formula": {},
                "teamV2": {},
                "enemy": {}
            },
            "crisis": {},
            "crisisV2": {},
            "nameCardStyle": {},
            "tshop": {},
            "gacha": {},
            "backflow": {},
            "mainline": {},
            "avatar": {
                "avatar_icon": {}
            },
            "background": {
                "selected": "bg_rhodes_flower_1",
                "bgs":{}
            },
            "homeTheme": {
                "selected": "tm_rogue_3",
                "themes":{}
            },
            "rlv2": rlv2,
            "deepSea": {},
            "tower": {},
            "siracusaMap": {},
            "sandboxPerm": {},
            "storyreview": {},
            "medal": {},
            "share": {},
            "charm": {},
            "campaignsV2": {
                "campaignCurrentFee": 1800,
                "campaignTotalFee": 1800,
                "open": {
                    "permanent":[],
                    "rotate":"",
                    "rGroup":"",
                    "training":[],
                    "tGroup":"",
                    "tAllOpen":None
                },
                "instances": {},
                "missions": {},
                "lastUpdateTs": 0,
                "lastRefreshTs": ts,
                "sweepMaxKills": {}
            },
            "retro": {
                "coin": 2,
                "supplement": 0,
                "block": {},
                "trail": {},
                "lst": ts,
                "nst": ts,
                "rewardPerm": [],
            },
            "recruit": {},
            "limitedBuff": {},
            "inventory": {},
            "event": {},
            "collectionReward": {},
            "setting": {},
            "ticket": {},
            "consumable": {},
            "car": {},
            "aprilFool": {},
            "checkIn": {},
            "openServer": {},
            "templateTrap": {},
            "roguelike": {},
            "carousel": {}
        },
        "playerDataDelta": {}
    }
    
    #Stage Unlock
    stage_table = read_json(STAGE_EXCEL_PATH)
    #print(stage_table["stages"])
    
    for stage in stage_table["stages"].values():
        newSyncData["user"]["dungeon"]["stages"][stage["stageId"]] = \
        {
            "stageId": stage["stageId"],
            "completeTimes": 1,
            "startTimes": 1,
            "practiceTimes": 1,
            "state": 3,
            "hasBattleReplay": 0,
            "noCostCnt": 1
        }
        if stage["stageType"] == "SPECIAL_STORY":
            unlock_condition = stage["extraCondition"]
            val = []
            for condition in unlock_condition:
                match condition["template"]:
                    case "PassStageWithChar":
                        val.append(True)
                    case "ReadStorySome":
                        tmp = []
                        for i in range(len(condition["unlockParam"])):
                            tmp.append(int(condition["unlockParam"][1]))
                        val.append(tmp)
                        
            newSyncData["user"]["dungeon"]["cowLevel"][stage["stageId"]] = \
            {
                "id": stage["stageId"],
                "type": "STAGE",
                "val": val,
                "fts": ts,
                "rts": ts
            }
    newSyncData["user"]["dungeon"]["hideStages"] = \
    {
        "act19side_s01": {
            "missions": [
                {
                    "value": 1,
                    "target": 1
                },
                {
                    "value": 1,
                    "target": 1
                }
            ],
            "unlock": 1
        },
        "act19side_s02": {
            "missions": [
                {
                    "value": 1,
                    "target": 1
                },
                {
                    "value": 1,
                    "target": 1
                }
            ],
            "unlock": 1
        }
    }

    #Activity TODO.JPG
    #Status
    story_table = read_json(STORY_EXCEL_PATH)
    flags = {
        "init": 1
    }
    for story in story_table.values():
        if story["repeatable"] != True:
            flags[story["id"]] = 1
    
    
    newSyncData["user"]["status"] = \
    {
        "nickName": "Dorothy",
        "nickNumber": rd(1,100000),
        "level": 120,
        "exp": 0,
        "socialPoint": 0,
        "gachaTicket": 114514,
        "tenGachaTicket": 114514,
        "instantFinishTicket": 9999,
        "hggShard": 0,
        "lggShard": 0,
        "recruitLicense": 9999,
        "progress": 30000,
        "buyApRemainTimes": 10,
        "apLimitUpFlag": 0,
        "uid": str(uid),
        "ap": 135,
        "maxAp": 135,
        "androidDiamond": 70,
        "iosDiamond": 1,
        "diamondShard": 90000,
        "gold": 983,
        "practiceTicket": 30,
        "lastRefreshTs": ts,
        "lastApAddTime": ts,
        "mainStageProgress": None,
        "registerTs": ts,
        "lastOnlineTs": ts,
        "serverName": "359号实验室",
        "avatarId": "0",
        "avatar": {
            "type": "ICON",
            "id": "avatar_def_15"
        },
        "resume": "Dorothinights",
        "friendNumLimit": 100,
        "monthlySubscriptionStartTime": 0,
        "monthlySubscriptionEndTime": 0,
        "secretary": "char_4048_doroth",
        "secretarySkinId": "char_4048_doroth#1",
        "tipMonthlyCardExpireTs": 0,
        "globalVoiceLan": "JP",
        "classicShard": 0,
        "classicGachaTicket": 0,
        "classicTenGachaTicket": 0,
        "flags": flags
    }
    
    
    #Chars(Troops) & Skins
    #(以下为odpy改)
    skin_table = read_json(SKIN_EXCEL_PATH)
    char_table = read_json(CHAR_EXCEL_PATH)
    equip_table = read_json(UNIEQUIP_EXCEL_PATH)
    
    skinKeys = list(skin_table["charSkins"].keys())
    skins = {}
    tmp_skins = {}
    char_group = {}
    char_list = {}
    cnt = 0
    cntInstId = 1
    maxInstId = 1
    for i in skin_table["charSkins"].values():
        if "@" not in skinKeys[cnt]:
            cnt += 1
            continue
        
        skins[skinKeys[cnt]] = 1
        if not i["charId"] in tmp_skins.keys() \
                or i["displaySkin"]["onYear"] > skin_table["charSkins"][tmp_skins[i["charId"]]]["displaySkin"]["onYear"]:
            tmp_skins[i["charId"]] = i["skinId"]
        cnt += 1
    cnt = 0
    operatorKeys = list(char_table.keys())
    equip_keys = list(equip_table["charEquip"].keys())
    for operatorKey in operatorKeys:
        if "char" not in operatorKey:
            continue

        char_group.update({
            operatorKey: {
                "favorPoint": 25570
            }
        })
    for i in char_table:
        if "char" not in operatorKeys[cnt]:
            cnt += 1
            continue

        level = char_table[i]["phases"][-1]["maxLevel"]


        maxEvolvePhase = len(char_table[i]["phases"]) - 1
        evolvePhase = maxEvolvePhase
        cntInstId = int(operatorKeys[cnt].split('_')[1])
        maxInstId = max(maxInstId, cntInstId)
        voiceLan = "JP"
        char_list[int(cntInstId)] = {
            "instId": int(cntInstId),
            "charId": operatorKeys[cnt],
            "favorPoint": 25570,
            "potentialRank": 5,
            "mainSkillLvl": 7,
            "skin": str(operatorKeys[cnt]) + "#1",
            "level": level,
            "exp": 0,
            "evolvePhase": evolvePhase,
            "defaultSkillIndex": len(char_table[i]["skills"])-1,
            "gainTime": int(time()),
            "skills": [],
            "voiceLan": voiceLan,
            "currentEquip": None,
            "equip": {},
            "starMark": 0,
            "profession": char_table[i]["profession"],
            "rarity": char_table[i]["rarity"].split("_")[1]
        }

        # set to E2 art if available skipping is2 recruits
        if operatorKeys[cnt] not in ["char_508_aguard", "char_509_acast", "char_510_amedic", "char_511_asnipe"]:
            if char_list[int(cntInstId)]["evolvePhase"] == 2:
                char_list[int(cntInstId)]["skin"] = str(operatorKeys[cnt]) + "#2"

        # set to seasonal skins
        if operatorKeys[cnt] in tmp_skins.keys():
            char_list[int(cntInstId)]["skin"] = tmp_skins[operatorKeys[cnt]]

        # Add Skills
        for index, skill in enumerate(char_table[i]["skills"]):
            char_list[int(cntInstId)]["skills"].append({
                "skillId": skill["skillId"],
                "unlock": 1,
                "state": 0,
                "specializeLevel": 0,
                "completeUpgradeTime": -1
            })

            # M3
            if len(skill["levelUpCostCond"]) > 0:
                char_list[int(cntInstId)]["skills"][index]["specializeLevel"] = 3

        # Add equips
        if char_list[int(cntInstId)]["charId"] in equip_keys:

            for equip in equip_table["charEquip"][char_list[int(cntInstId)]["charId"]]:
                level = 3
                if equip in list(equip_table.keys()):
                    level = len(equip_table[equip]["phases"])
                char_list[int(cntInstId)]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": level
                    }
                })
            char_list[int(cntInstId)]["currentEquip"] = equip_table["charEquip"][char_list[int(cntInstId)]["charId"]][-1]

        # Dexnav
        newSyncData["user"]["dexNav"]["character"][operatorKeys[cnt]] = {
            "charInstId": cntInstId,
            "count": 6
        }


        if operatorKeys[cnt] == "char_002_amiya":
            char_list[int(cntInstId)].update({
                "defaultSkillIndex": -1,
                "skills": [],
                "currentTmpl": "char_002_amiya",
                "tmpl": {
                    "char_002_amiya": {
                        "skinId": "char_002_amiya@test#1",
                        "defaultSkillIndex": 2,
                        "skills": [
                            {
                                "skillId": skill_name,
                                "unlock": 1,
                                "state": 0,
                                "specializeLevel": 3,
                                "completeUpgradeTime": -1
                            } for skill_name in ["skcom_magic_rage[3]", "skchr_amiya_2", "skchr_amiya_3"]
                        ],
                        "currentEquip": None,
                        "equip": {},
                    },
                    "char_1001_amiya2": {
                        "skinId": "char_1001_amiya2@casc#1",
                        "defaultSkillIndex": 1,
                        "skills": [
                            {
                                "skillId": skill_name,
                                "unlock": 1,
                                "state": 0,
                                "specializeLevel": 3,
                                "completeUpgradeTime": -1
                            } for skill_name in ["skchr_amiya2_1", "skchr_amiya2_2"]
                        ],
                        "currentEquip": None,
                        "equip": {},
                    },
                    "char_1037_amiya3": {
                        "skinId": "char_1037_amiya3#2",
                        "defaultSkillIndex": 1,
                        "skills": [
                            {
                                "skillId": skill_name,
                                "unlock": 1,
                                "state": 0,
                                "specializeLevel": 3,
                                "completeUpgradeTime": -1
                            } for skill_name in ["skchr_amiya3_1", "skchr_amiya3_2"]
                        ],
                        "currentEquip": None,
                        "equip": {},
                    }
                }
            })
            for equip in equip_table["charEquip"]["char_002_amiya"]:
                level = 1
                if equip in list(equip_table.keys()):
                    level = len(equip_table[equip]["phases"])
                char_list[int(cntInstId)]["tmpl"]["char_002_amiya"]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": level
                    }
                })
            char_list[int(cntInstId)]["tmpl"]["char_002_amiya"]["currentEquip"] = equip_table["charEquip"]["char_002_amiya"][-1]
            for equip in equip_table["charEquip"]["char_1037_amiya3"]:
                level = 1
                if equip in list(equip_table.keys()):
                    level = len(equip_table[equip]["phases"])
                char_list[int(cntInstId)]["tmpl"]["char_1037_amiya3"]["equip"].update({
                    equip: {
                        "hide": 0,
                        "locked": 0,
                        "level": level
                    }
                })
            char_list[int(cntInstId)]["tmpl"]["char_1037_amiya3"]["currentEquip"] = equip_table["charEquip"]["char_1037_amiya3"][-1]
        elif operatorKeys[cnt] == "char_512_aprot":
            char_list[int(cntInstId)]["skin"] = "char_512_aprot#1"


        """buildingChars.update({
            int(cntInstId): {
                "charId": operatorKeys[cnt],
                "lastApAddTime": round(time()) - 3600,
                "ap": 8640000,
                "roomSlotId": "",
                "index": -1,
                "changeScale": 0,
                "bubble": {
                    "normal": {
                        "add": -1,
                        "ts": 0
                    },
                    "assist": {
                        "add": -1,
                        "ts": 0
                    }
                },
                "workTime": 0
            }
        })"""

        cnt += 1
    cntInstId = 10000

    block = {}
    retro_table = read_json(RETRO_EXCEL_PATH)
    for retro in retro_table["retroActList"]:
        block.update({
            retro: {
                "locked": 0,
                "open": 1
            }
        })
    newSyncData["user"]["retro"]["block"] = block
    trail = {}
    for retro in retro_table["retroTrailList"]:
        trail.update({retro:{}})
        for trailReward in retro_table["retroTrailList"][retro]["trailRewardList"]:
            trail[retro][trailReward["trailRewardId"]] = 1
    newSyncData["user"]["retro"]["trail"] = trail
    
    for stage in stage_table["stages"]:
        if stage.startswith("camp"):
            newSyncData["user"]["campaignsV2"]["instances"].update({
                stage: {
                    "maxKills": 400,
                    "rewardStatus": [1, 1, 1, 1, 1, 1, 1, 1]
                }
            })

            newSyncData["user"]["campaignsV2"]["sweepMaxKills"].update({stage: 400})
            newSyncData["user"]["campaignsV2"]["open"]["permanent"].append(stage)
            newSyncData["user"]["campaignsV2"]["open"]["training"].append(stage)
            
            
            
    avatar_icon = {}
    display_meta_table = read_json(DISPLAY_META_EXCEL_PATH)
    
    for avatar in display_meta_table["playerAvatarData"]["avatarList"]:
        avatar_icon.update({
            avatar["avatarId"]: {
                "ts": ts,
                "src": "initial" if avatar["avatarId"].startswith("avatar_def") else "other"
            }
        })
    newSyncData["user"]["avatar"]["avatar_icon"] = avatar_icon
    bgs = {}
    for bg in display_meta_table["homeBackgroundData"]["homeBgDataList"]:
        bgs.update({
            bg["bgId"]: {
                "unlock": ts
            }
        })
    newSyncData["user"]["background"]["bgs"] = bgs
    if "themeList" in display_meta_table["homeBackgroundData"]:
        themes = {}
        for theme in display_meta_table["homeBackgroundData"]["themeList"]:
            themes[theme["id"]] = {
                "unlock": ts
            }
        newSyncData["user"]["homeTheme"]["themes"] = themes
    addonList = {}
    addon_table = read_json(HANDBOOK_INFO_EXCEL_PATH)
    for charId in addon_table["handbookDict"]:
        addonList[charId] = {"story":{}}
        story = addon_table["handbookDict"][charId]["handbookAvgList"]
        for i,j in zip(story,range(len(story))):
            if "storySetId" in i:
                addonList[charId]["story"].update({
                    addon_table["handbookDict"][charId]["handbookAvgList"][j]["storySetId"]: {
                        "fts": 1649232340,
                        "rts": 1649232340
                    }
                })
    
    story_review_table = read_json(STORY_REVIEW_EXCEL_PATH)
    story_review_meta_table = read_json(STORY_REVIEW_META_EXCEL_PATH)
    story_review_groups = {}
    for i in story_review_table:
        story_review_groups[i] = {
            "rts": 1700000000,
            "stories": [],
            "trailRewards": []
        }
        for j in story_review_table[i]["infoUnlockDatas"]:
            story_review_groups[i]["stories"].append(
                {
                    "id": j["storyId"],
                    "uts": 1695000000,
                    "rc": 1
                }
            )
        if i in story_review_meta_table["miniActTrialData"]["miniActTrialDataMap"]:
            for j in story_review_meta_table["miniActTrialData"]["miniActTrialDataMap"][i]["rewardList"]:
                story_review_groups[i]["trailRewards"].append(
                    j["trialRewardId"]
                )
    newSyncData["user"]["storyreview"]["groups"] = story_review_groups
    
    enemy_handbook_table = read_json(ENEMY_HANDBOOK_EXCEL_PATH)
    enemies = {}
    if "enemyData" in enemy_handbook_table:
        for i in enemy_handbook_table["enemyData"]:
            enemies[i] = 1
    else:
        for i in enemy_handbook_table:
            enemies[i] = 1
    newSyncData["user"]["dexNav"]["enemy"]["enemies"] = enemies

    activity_table = read_json(ACTIVITY_EXCEL_PATH)
    
    for i in activity_table["activity"]:
        if i not in newSyncData["user"]["activity"]:
            newSyncData["user"]["activity"][i] = {}
        for j in activity_table["activity"][i]:
            if j not in newSyncData["user"]["activity"][i]:
                newSyncData["user"]["activity"][i][j] = {}

    newSyncData["user"]["medal"] = {"medals": {}}
    medal_table = read_json(MEDAL_EXCEL_PATH)
    for i in medal_table["medalList"]:
        medalId = i["medalId"]
        newSyncData["user"]["medal"]["medals"][medalId] = {
            "id": medalId,
            "val": [],
            "fts": 1695000000,
            "rts": 1695000000
        }
    
    newSyncData["user"]["troop"]["chars"] = char_list
    newSyncData["user"]["troop"]["charGroup"] = char_group
    newSyncData["user"]["troop"]["curCharInstId"] = cntInstId
    
    
    return newSyncData