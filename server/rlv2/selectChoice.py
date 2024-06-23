from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueSelectChoice


@post("/selectChoice")
async def selectChoice(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    choose = request_data["choice"]
    rogue = await rogueSelectChoice(secret, choose)
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