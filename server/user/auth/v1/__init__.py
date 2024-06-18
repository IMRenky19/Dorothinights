from .token_by_phone_password import tokenByPhonePassword
from litestar import Router

router = Router(
    path = "/v1",
    route_handlers = [
        tokenByPhonePassword
    ]
)
