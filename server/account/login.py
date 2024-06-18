from litestar import get, Response, post, Request
from json import load

@post("/login")
async def login(request: Request, response: Response) -> Response:
    request_data = load(request)
    uid = request_data["uid"]
    token = request_data["token"]
    return Response(
        content = {
            "result":0,
            "uid":uid,
            "secret":token,
            "serviceLicenseVersion":0,
            "majorVersion":"325"
        }
    )