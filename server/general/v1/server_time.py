from litestar import Router, get, Response
import time

@get("/server_time")
async def server_time() -> Response:
    time_tmp = time.time()
    current_time: int = int(time_tmp)
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