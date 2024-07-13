from litestar import Request, Response, post
from server.core.database.function.rogueData import getRogueBySecret
from server.core.database.function.rogueData import giveUpRogue
from math import floor

@post("/gameSettle")
async def gameSettle(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await getRogueBySecret(secret)
    rogueData = rogue.rlv2
    rogueExtensionData = rogue.extension
    
    endData = rogueData["current"]["player"]["pending"][0]["content"]["result"]
    zoneCnt = endData["record"]["cntZone"]
    match zoneCnt:
        case 0:
            zoneScore = 0
        case 1:
            zoneScore = 30
        case 2:
            zoneScore = 80
        case 3:
            zoneScore = 150
        case 4:
            zoneScore = 270
        case 5:
            zoneScore = 400
        case 6:
            zoneScore = 550
        case zoneCnt if zoneCnt >= 7:
            zoneScore = 650
    stepCount = endData["record"]["cntArrivedNode"]
    stepScore = stepCount * 1
    recruitRealCount = endData["record"]["recruitRealCount"]
    recruitScore = recruitRealCount * 2
    itemCount = endData["record"]["itemCount"]
    itemScore = itemCount * 5
    bossCount = endData["record"]["cntBattleBoss"]
    bossScore = bossCount * 30
    eliteCount = endData["record"]["cntBattleElite"]
    eliteScore = eliteCount * 20
    normalCount = endData["record"]["cntBattleNormal"]
    normalScore = normalCount * 10
    
    totalBaseScore = stepScore + recruitScore + itemScore + bossScore + eliteScore + normalScore + zoneScore
    
    endData["score"] = {
        "detail": [
                [
                    endData["record"]["cntZone"],
                    zoneScore
                ],
                [
                    stepCount,
                    stepScore
                ],
                [
                    normalCount,
                    normalScore
                ],
                [
                    eliteCount,
                    eliteScore
                ],
                [
                    bossCount,
                    bossScore
                ],
                [
                    itemCount,
                    itemScore
                ],
                [
                    recruitRealCount,
                    recruitScore
                ]
            ],
            "scoreFactor": rogueExtensionData["score_multiplier"],
            "score": floor(totalBaseScore * rogueExtensionData["score_multiplier"]),
            "buff": 1 + rogueExtensionData["extra_grow_point"],
            "bp": {
                "cnt": floor(floor(totalBaseScore * rogueExtensionData["score_multiplier"]) * (1 + rogueExtensionData["extra_grow_point"])),
                "from": 55000,
                "to": 55000
            },
            "gp": 0,
            "gpChange": [
                100,
                100
            ],
            "accumulation": [
                20000,
                20000
            ]
    }
    await giveUpRogue(secret)
    
    return Response(
        content= {
            "game":endData,
            "outer":{           #TODO
                "mission":{
                    "before":[],
                    "after":[]
                },
                "missionBp":{
                    "cnt":0,
                    "from":55000,
                    "to":55000
                },
                "relicBp":{
                    "cnt":0,
                    "from":55000,
                    "to":55000
                },
                "totemBp":{
                    "cnt":0,
                    "from":55000,
                    "to":55000
                },
                "relicUnlock":[],
                "totemUnlock":[],
                "gp":0
            },
            "playerDataDelta":{
                "modified":{
                    "rlv2": {
                        "current": {
                            "player": None, 
                            "record": None, 
                            "map": None, 
                            "troop": None, 
                            "inventory": None, 
                            "game": None, 
                            "buff": None, 
                            "module": None
                            }
                        }
                    },
                },
                "deleted":{}
        }
    )