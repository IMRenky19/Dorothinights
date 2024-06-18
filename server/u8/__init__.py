from . import pay, user
from litestar import Router

router = Router(
    path = "/u8",
    route_handlers = [
        pay.router,
        user.router
    ]
)
