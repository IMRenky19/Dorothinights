from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueRefreshShop


@post("/refreshShop")
async def refreshShop(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await rogueRefreshShop(secret)
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