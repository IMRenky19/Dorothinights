from litestar import Router, get, Response
from time import time

@get("/server_time")
async def server_time() -> Response:
    current_time: int = int(time)
    return Response(
        content = {
            "data": {
                "serverTime": current_time,
                "isHoliday": False
            },
            "msg": "OK",
            "status":0,
            "type":"A"
        }
    )