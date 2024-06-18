from litestar import Litestar
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyInitPlugin
from server.core.database.function.init import initDatabase, sqlalchemy_config

from . import config, general, user, u8, app, account
app = Litestar(
    route_handlers=[
        config.router,
        general.router,
        user.router,
        u8.router,
        app.router,
        account.router
    ],
    on_startup=[initDatabase],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    debug=True,
)