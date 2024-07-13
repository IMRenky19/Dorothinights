from litestar import Request, post, Response


@post("/finishStory")
async def finishStory(request: Request) -> Response:
    return Response(
        content = {
            "playerDataDelta":{
                "modified":{},
                "deleted":{}}
        }
    )