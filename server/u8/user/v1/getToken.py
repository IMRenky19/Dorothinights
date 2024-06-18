from litestar import post, Request, Response
from json import loads
from server.core.database.function.userData import getAccountBySecret

@post("/getToken")
async def getToken(request: Request) -> Response:
    request_data = await request.json()
    token: str = loads(request_data["extension"])["code"]
    temp = await getAccountBySecret(token)
    if account := temp:
        return Response(
            content = {
                "result":0,
                "error":"",
                "uid":temp.uid,
                "channelUid":"1145141919810",
                "token":token,
                "isGuest":0,
                "extension":"{\"isMinor\":false,\"isAuthenticate\":true}"
            }
        )
    else:
        raise Exception