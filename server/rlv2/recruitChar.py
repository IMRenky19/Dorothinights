from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueRecruitChar


@post("/recruitChar")
async def recruitChar(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    choice = request_data["optionId"]
    ticketId = request_data["ticketIndex"]
    rogue = await rogueRecruitChar(secret, ticketId, choice)
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