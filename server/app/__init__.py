from . import v1
from litestar import Router

router = Router(
    path = "/app",
    route_handlers = [
        v1.router
    ]
)
