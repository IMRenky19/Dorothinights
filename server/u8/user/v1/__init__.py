from .getToken import getToken
from litestar import Router

router = Router(
    path = "/v1",
    route_handlers = [
        getToken
    ]
)