from . import v2
from litestar import Router

router = Router(
    path = "/oauth2",
    route_handlers = [
        v2.router
    ]
)
