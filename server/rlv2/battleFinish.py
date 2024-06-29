from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueBattleFinish

@post("/battleFinish")
async def battleFinish(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    battleData = request_data["data"]
    rogue = await rogueBattleFinish(secret, battleData)
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