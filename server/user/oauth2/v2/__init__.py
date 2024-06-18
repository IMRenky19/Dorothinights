from .grant import grant
from litestar import Router

router = Router(
    path = "/v2",
    route_handlers = [
        grant
    ]
)
