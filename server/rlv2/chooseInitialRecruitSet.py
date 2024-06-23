from litestar import Request, Response, post
from server.core.database.function.rogueData import rogueChooseInitialRecruitSet


@post("/chooseInitialRecruitSet")
async def chooseInitialRecruitSet(request: Request) -> Response:
    request_data = await request.json()
    secret = request.headers["Secret"]
    choose = request_data["select"]
    rogue = await rogueChooseInitialRecruitSet(secret, choose)
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