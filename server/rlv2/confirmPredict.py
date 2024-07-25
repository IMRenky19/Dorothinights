from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueConfirmPredict


@post("/confirmPredict")
async def confirmPredict(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await rogueConfirmPredict(secret)
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