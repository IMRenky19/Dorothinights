from litestar import post, Request, Response
from json import load
from server.core.database.function.userData import getAccountBySecret

@post("/getToken")
async def getToken(request: Request, response: Response) -> Response:
    request_data: dict = load(request)
    token: str = load(request_data["extension"])["code"]
    if account := getAccountBySecret(token):
        return Response(
            content = {
                "result":0,
                "error":"",
                "uid":account.uid,
                "channelUid":"1145141919810",
                "token":token,
                "isGuest":0,
                "extension":"{\"isMinor\":false,\"isAuthenticate\":true}"
            }
        )
    else:
        raise Exception