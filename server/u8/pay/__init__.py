from .getAllProductList import getAllProductList
from litestar import Router

router = Router(
    path = "/pay",
    route_handlers = [
        getAllProductList
    ]
)
