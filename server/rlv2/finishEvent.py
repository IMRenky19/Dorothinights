from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueFinishEvent


@post("/finishEvent")
async def finishEvent(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    rogue = await rogueFinishEvent(secret)
    #match rogue.extension["isPredict"]:
    #    case "chaos":
    #        deleted = {
    #            "rlv2":{
    #                "current":{
    #                    "module":{
    #                        "totem":["predict"]
    #                    }
    #                }
    #            }
    #        }
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