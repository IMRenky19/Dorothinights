from .config import networkConfig, remoteConfig, version
    
from litestar import Router

router = Router(
    path = "/official",
    route_handlers = [
        networkConfig,
        remoteConfig,
        version,
    ]
)

