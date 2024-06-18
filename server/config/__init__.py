from . import prod
from litestar import Router

router = Router(
    path = "/config",
    route_handlers = [
        prod.router
    ]
)

