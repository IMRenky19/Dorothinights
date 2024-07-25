from litestar import Request, Response, post
from server.core.database.function.rogueData import generateRogueData


@post("/createGame")
async def createGame(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    
    theme = request_data["theme"]
    hardLevel = request_data["modeGrade"]
    rogue = await generateRogueData(theme, hardLevel, secret)
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