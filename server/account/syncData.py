from litestar import Request, post, Response
from server.core.database.function.userData import getAccountBySecret, writeAccountSyncData
from server.core.utils.accounts import generateNewSyncData
from server.core.utils.time import time
from server.core.database.function.userData import show_secret
from json import loads


@post("/syncData")
async def syncData(request: Request) -> Response:
    secret = request.headers["Secret"]
    account = await getAccountBySecret(secret)
    #print(account.user)
    #if account.user == {}:
    syncdata = await generateNewSyncData(account.uid)
    await writeAccountSyncData(secret, syncdata)
    return Response(
        content = syncdata
    )
    """else:
        ts = time()
        syncdata = account.user
        syncdata["status"]["lastRefreshTs"] = ts
        syncdata["status"]["lastApAddTime"] = ts
        syncdata["status"]["registerTs"] = ts
        syncdata["status"]["lastOnlineTs"] = ts
        syncdata["crisis"]["lst"] = ts
        syncdata["crisis"]["nst"] = ts + 3600
        return Response(
            content = {
                "result": 0,
                "ts": ts,
                "user": account.user
            }
        )"""