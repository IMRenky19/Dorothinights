from litestar import Request, post, Response
from server.core.database.function.userData import getAccountBySecret, writeAccountSyncData
from server.core.utils.accounts import generateNewSyncData
from server.core.utils.time import time
from json import loads


@post("/syncPushMessage")
async def syncPushMessage(request: Request) -> Response:
    return Response(
        content = {
            "playerDataDelta":{
                "modified":{},
                "deleted":{}
            },
            "pushMessage":[
                {
                    "path":"flushAlerts",
                    "payload":{
                        "data":"{\"content\":\"<color=#ff0000>Dorothinights</color><color=#00ff7f>肉鸽锐意制作中...</color>\",\"loop\":4,\"majorVersion\":\"326\"}"
                    }
                }
            ]
        }
    )