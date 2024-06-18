from . import v1
from litestar import Router

router = Router(
    path = "/info",
    route_handlers = [
        v1.router
    ]
)
