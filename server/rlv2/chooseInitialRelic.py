from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueChooseInitialRelic


@post("/chooseInitialRelic")
async def chooseInitialRelic(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    choose = request_data["select"]
    rogue = await rogueChooseInitialRelic(secret, choose)
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