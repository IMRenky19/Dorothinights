from litestar import Request, Response, post
from server.core.database.function.rogueData import giveUpRogue
from server.core.database.function.userData import deleteRogueData


@post("/giveUpGame")
async def giveUpGame(request: Request) -> Response:
    
    secret = request.headers["Secret"]
    await giveUpRogue(secret)    
    
    content = {
        "result": "ok", 
        "playerDataDelta": {
            "modified": {
                "rlv2": {
                    "current": {
                        "player": None, 
                        "record": None, 
                        "map": None, 
                        "troop": None, 
                        "inventory": None, 
                        "game": None, 
                        "buff": None, 
                        "module": None
                        }
                    }
                }, 
            "deleted": {}
            }
    }  
    
    #content.update(rogue.extension["extraResponse"])
    return Response(
        content = content
    )