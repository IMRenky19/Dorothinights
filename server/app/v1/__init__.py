from .config import config
from litestar import Router

router = Router(
    path = "/v1",
    route_handlers = [
        config
    ]
)
