from . import official
from litestar import Router

router = Router(
    path = "/prod",
    route_handlers = [
        official.router
    ]
)

