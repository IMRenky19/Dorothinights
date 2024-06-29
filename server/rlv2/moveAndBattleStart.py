from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueMoveAndBattleStart
from uuid import uuid1

@post("/moveAndBattleStart")
async def moveAndBattleStart(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    position = request_data["to"]
    rogue = await rogueMoveAndBattleStart(secret, position)
    return Response(
        content= {
            "battleId":uuid1(),
            "playerDataDelta":{
                "modified":{
                    "rlv2":rogue.rlv2
                },
                "deleted":{}
            }
        } 
    )