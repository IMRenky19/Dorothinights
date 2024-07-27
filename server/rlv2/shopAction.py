from litestar import Request, Response, post
from server.core.database.function.rogueData import getRogueBySecret, rogueBuyGoods, rogueLeaveShop

@post("/shopAction")
async def shopAction(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    if request_data["leave"]:
        rogue = await rogueLeaveShop(secret)
    elif request_data["buy"]:
        choice = int(request_data["buy"][0])
        rogue = await rogueBuyGoods(secret, choice)
    else:
        rogue = await rogueLeaveShop(secret)
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