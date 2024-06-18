from .server_time import server_time
from litestar import Router

router = Router(
    path = "/v1",
    route_handlers = [
        server_time
    ]
)
