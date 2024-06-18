from . import v1
from litestar import Router

router = Router(
    path = "/general",
    route_handlers = [
        v1.router
    ]
)
