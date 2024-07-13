from litestar import Request, Response, post
from server.core.database.function.rogueData import getRogueBySecret, rogueBuyGoods, rogueLeaveShop

@post("/shopAction")
async def shopAction(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    if request_data["leave"]:
        rogue = await rogueLeaveShop(secret)
    elif request_data["buy"]:
        choice = int(request_data["buy"][0])
        rogue = await rogueBuyGoods(secret, choice)
    elif request_data["recycle"]:
        pass    #TODO:萨卡兹肉鸽出售藏品/思绪功能
    
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