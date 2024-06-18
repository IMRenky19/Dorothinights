from .login import login
from litestar import Router

router = Router(
    path = "/account",
    route_handlers = [
        login
    ]
)
