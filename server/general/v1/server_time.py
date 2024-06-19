from litestar import Router, get, Response
from server.core.utils.time import time

@get("/server_time")
async def server_time() -> Response:
    return Response(
        content = {
            "data": {
                "serverTime": time(),
                "isHoliday": False
            },
            "msg": "OK",
            "status":0,
            "type":"A"
        }
    )