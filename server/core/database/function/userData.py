from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
from server.core.Model.RogueBase import RogueBasicModel
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig
from sqlalchemy import select
from server.core.utils.json import read_json
from random import randint as rd
from copy import deepcopy
from server.constants import CONFIG_PATH
import hashlib
from time import time
from contextlib import asynccontextmanager


USER_TOKEN_KEY = "d0r0th1n1ghts123"
session_config = AsyncSessionConfig(expire_on_commit=False)
database_config = read_json(CONFIG_PATH)["database"]
db_user = database_config["user"]
db_password = database_config["password"]
db_host = database_config["host"]
db_port = database_config["port"]

async def get_sqlalchemy_config() -> SQLAlchemyAsyncConfig:
    sqlalchemy_config = SQLAlchemyAsyncConfig(
                connection_string=f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/arknights", 
                session_config=session_config
            )
    return sqlalchemy_config

@asynccontextmanager
async def get_db_session():
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

async def generateUsers(phone: str, password: str) -> Account:
    secret: str = hashlib.md5((phone + decrypt_user_key(USER_TOKEN_KEY, int(time()))).encode()).hexdigest()
    async with get_db_session() as session:
        new_user = Account(
            uid=rd(10000000,1000000000),
            phone=phone,
            password=password,
            secret=secret,
            user={},
            mails={},
            assist_char_list={},
            friend={
                'list':[],
                'request':[]
            },
            ban=0,
            notes="",
            currentRogue=""
        )
        session.add(new_user)
    return new_user

async def getAccountBySecret(secret: str) -> Account:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return Account()
        else:
            return account

async def getAccountByPhone(phone: str) -> Account:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.phone == phone)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return Account()
        else:
            return account

async def getAccountByUid(uid: str | int) -> Account:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.uid == int(uid))
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return Account()
        else:
            return account

async def writeAccountSyncData(secret: str, syncdata: dict) -> None:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return None
        else:
            account.user = syncdata["user"]

async def syncRogueData(rogue: RogueBasicModel, secret: str) -> None:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return None
        else:
            tmp_1 = deepcopy(account.user)
            if not(rogue.rlv2):
                tmp_1["rlv2"]["current"] = {}
                account.currentRogue = ""
            else:
                tmp_1["rlv2"] = rogue.rlv2
                account.currentRogue = rogue.rlv2["current"]["game"]["theme"] if rogue.rlv2 else ""
            account.user = tmp_1

async def deleteRogueData(secret: str) -> None:
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return None
        else:
            account.user["rlv2"]["current"] = {}
            account.currentRogue = ""

async def updateAccount(secret: str):
    async with get_db_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        if not account:
            return None
        else:
            syncdata = deepcopy(account.user)
            ts = int(time())
            syncdata["status"]["lastRefreshTs"] = ts
            syncdata["status"]["lastApAddTime"] = ts
            syncdata["status"]["lastOnlineTs"] = ts
            syncdata["crisis"]["lst"] = ts
            syncdata["crisis"]["nst"] = ts + 3600
            syncdata["pushFlags"]["status"] = ts
            account.user = syncdata