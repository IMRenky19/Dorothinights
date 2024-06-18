from litestar import get, Request, Response, post
from json import load
from server.core.database.function.userData import getAccountByPhone, generateUsers


@post("/token_by_phone_password")
async def tokenByPhonePassword(request: Request, response: Response) -> Response:
    phone = load(request)["phone"]
    if account := getAccountByPhone(phone):
        account = generateUsers(phone, load(request)["password"])
    return Response(
        content = {
            "data":{
                "token": account.secret
            },
            "msg": "OK",
            "status": 0,
            "type": "A"
        }
    )