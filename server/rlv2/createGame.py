from litestar import Request, Response, post
from server.core.database.function.rogueData import generateRogueData


@post("/createGame")
async def createGame(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    
    theme = request_data["theme"]
    print(theme)
    hardLevel = request_data["modeGrade"]
    rogue = await generateRogueData(theme, hardLevel, secret)
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