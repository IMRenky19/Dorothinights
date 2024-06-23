from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueFinishEvent


@post("/finishEvent")
async def finishEvent(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await rogueFinishEvent(secret)
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