from . import auth, info, oauth2
from litestar import Router

router = Router(
    path = "/user",
    route_handlers = [
        auth.router,
        info.router,
        oauth2.router
    ]
)
