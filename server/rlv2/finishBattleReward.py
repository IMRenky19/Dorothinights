from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueFinishBattleReward

@post("/finishBattleReward")
async def finishBattleReward(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await rogueFinishBattleReward(secret)
    content= {
        "playerDataDelta":{
            "modified":{
                "rlv2":rogue.rlv2
            },
            "deleted":{}
        }
    }
    content.update(rogue.extension["extraResponse"])
    return Response(
        content = content
    )