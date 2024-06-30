from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueChooseBattleReward

@post("/chooseBattleReward")
async def chooseBattleReward(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    index = request_data["index"]
    sub = request_data["sub"]
    rogue = await rogueChooseBattleReward(secret, index, sub)
    return Response(
        content= {
            "playerDataDelta":{
                "modified":{
                    "rlv2":rogue.rlv2
                },
                "deleted":{}
            }
        } 
    )