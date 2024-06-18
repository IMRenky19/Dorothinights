from litestar import post, Request, Response
from json import load

@post("/grant")
async def grant(request: Request) -> Response:
    request_data = await request.json()
    return Response(
        content = {
            "data":{
                "uid":"1145141919810",
                "code":request_data["token"]
            },
            "msg":"OK",
            "status":0,
            "type":"A"
        }
    )


