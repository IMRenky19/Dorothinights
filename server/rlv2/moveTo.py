from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueMoveTo

@post("/moveTo")
async def moveTo(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    position = request_data["to"]
    rogue = await rogueMoveTo(secret, position)
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