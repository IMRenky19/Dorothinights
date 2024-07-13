from .finishStory import finishStory
from litestar import Router

router = Router(
    path = "/story",
    route_handlers = [
        finishStory
    ]
)
