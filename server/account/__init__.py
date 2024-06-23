from .login import login
from .syncData import syncData
from .syncPushMessage import syncPushMessage
from litestar import Router

router = Router(
    path = "/account",
    route_handlers = [
        login,
        syncData,
        syncPushMessage
    ]
)
