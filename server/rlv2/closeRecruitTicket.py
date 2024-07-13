from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueRecruitChar


@post("/closeRecruitTicket")
async def closeRecruitTicket(request: Request) -> Response:
    request_data = await request.json()
    print(request_data)
    secret = request.headers["Secret"]
    ticketId = request_data["id"]
    rogue = await rogueRecruitChar(secret, ticketId, None, isClose = True)
    char = rogue.rlv2["current"]["inventory"]["recruit"][ticketId]["result"]
    return Response(
        content= {
            "chars": [char],
            "playerDataDelta":{
                "modified":{
                    "rlv2":rogue.rlv2
                },
                "deleted":{}
            }
        } 
    )