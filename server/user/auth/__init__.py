from . import v1
from litestar import Router

router = Router(
    path = "/auth",
    route_handlers = [
        v1.router
    ]
)
