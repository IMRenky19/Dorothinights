from litestar import Request, Response, post

@post("/getUnconfirmedOrderIdList")
async def getUnconfirmedOrderIdList(request: Request) -> Response:
    return Response(
        content = {
            "orderIdList":[],
            "playerDataDelta":{
                "modified":{},
                "deleted":{}
            }
        }
    )