from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueUseTotem


@post("/useTotem")
async def useTotem(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    totemIndex = request_data["totemIndex"]
    nodeIndex = request_data["nodeIndex"]
    rogue = await rogueUseTotem(secret, totemIndex, nodeIndex)
    nodeIndex = rogue.extension["lastTotemNodeIndex"]
    return Response(
        content= {
            "nodeIndex": nodeIndex,
            "playerDataDelta":{
                "modified":{
                    "rlv2":rogue.rlv2
                },
                "deleted":{}
            }
        } 
    )