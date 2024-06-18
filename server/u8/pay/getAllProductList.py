from litestar import post, Request, Response
from json import load
from server.core.database.function.userData import getAccountBySecret

@post("/getAllProductList")
async def getAllProductList(request: Request) -> Response:
    return Response(
        content = {
            "productList":[]
        }
    )