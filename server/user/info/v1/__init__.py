from .basic import basic
from litestar import Router

router = Router(
    path = "/v1",
    route_handlers = [
        basic
    ]
)
