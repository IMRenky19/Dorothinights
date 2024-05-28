from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from server.core.database.function.init import initDatabase, sqlalchemy_config

app = Litestar(
    route_handlers=[],
    on_startup=[initDatabase],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
)