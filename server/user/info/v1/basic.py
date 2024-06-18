from litestar import get, Request, Response, post
from json import load
from server.core.database.function.userData import getAccountBySecret

@get("/basic")
async def basic(token: str) -> Response:
    account = await getAccountBySecret(token)
    if phone := account.phone:
        return Response(    
            content = {
                "data":{
                    "hgId":"1145141919810",
                    "phone":phone,
                    "email":"Dor**********@rhine.lab",
                    "identityNum":"1145**********1428",
                    "identityName":"多**",
                    "isMinor":False,
                    "isLatestUserAgreement":True
                },
                "msg":"OK",
                "status":0,
                "type":"A"
            }
        )
    else:
        raise Exception