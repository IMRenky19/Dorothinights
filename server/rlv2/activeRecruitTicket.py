from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueActiveRecruitTicket


@post("/activeRecruitTicket")
async def activeRecruitTicket(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    ticketId = request_data["id"]
    rogue = await rogueActiveRecruitTicket(secret, ticketId)
    
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