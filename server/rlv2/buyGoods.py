from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueBuyGoods


@post("/buyGoods")
async def buyGoods(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    choose = int(request_data["select"][0])
    rogue = await rogueBuyGoods(secret, choose)
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