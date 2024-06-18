from server.constants import CONFIG_PATH
from server.core.utils.json import read_json, write_json
from server.core.Model.User import AccountBase

from sqlalchemy import text

from litestar.contrib.sqlalchemy.base import UUIDAuditBase, UUIDBase
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin

database_config = read_json(CONFIG_PATH)["database"]
db_user = database_config["user"]
db_password = database_config["password"]
db_host = database_config["host"]
db_port = database_config["port"]
session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/arknights", 
    session_config=session_config
)
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)
#engine = create_engine(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/arknights",echo=database_config["enableLog"])
async def initDatabase() -> None:
    engine = SQLAlchemyAsyncConfig(
            connection_string=f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}", 
            session_config=session_config
        ).get_engine()
    async with engine.begin() as conn:
        await conn.execute(
            text("create database if not exists arknights;use arknights"))
        await conn.close()
    await engine.dispose()
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(AccountBase.metadata.create_all)