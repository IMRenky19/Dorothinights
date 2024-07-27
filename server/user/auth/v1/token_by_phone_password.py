from litestar import get, Request, Response, post
from json import load
from server.core.database.function.userData import getAccountByPhone, generateUsers


@post("/token_by_phone_password")
async def tokenByPhonePassword(request: Request) -> Response:
    request_data = await request.json()
    phone = request_data["phone"]
    tmp = await getAccountByPhone(phone)
    if not (account := tmp):
        account = await generateUsers(phone, request_data["password"])
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