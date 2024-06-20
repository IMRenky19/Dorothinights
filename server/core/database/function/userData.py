from server.core.database.function.init import sqlalchemy_config
from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
from server.core.Model.RogueBase import RogueBasicModel
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy import select
from sqlalchemy.orm import Session
from server.core.utils.json import read_json, write_json
from random import randint as rd
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
                session_config=session_config,
            )
    return sqlalchemy_config

async def generateUsers(phone: str, password: str) -> Account:
    config = await get_sqlalchemy_config()
    secret: str = hashlib.md5((phone + decrypt_user_key(USER_TOKEN_KEY, int(time()))).encode()).hexdigest()
    async with config.get_session() as session:
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
        print(session)
        session.add(new_user)
        await session.commit()
    return new_user


        
async def getAccountBySecret(secret: str) -> Account:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
    return result.scalar()

async def getAccountByPhone(phone: str) -> Account:
    #session: Session
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.phone == phone)
        result = await session.execute(user_cmd)
    return result.scalar()

async def getAccountByUid(uid: str | int) -> Account:
    #session: Session
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.uid == int(uid))
        result = await session.execute(user_cmd)
    return result.scalar()

async def writeAccountSyncData(secret: str, syncdata: dict) -> None:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        account.user = syncdata["user"]
        await session.commit()
    
#test
async def show_secret(phone: str) -> None:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.phone == phone)
        result = await session.execute(user_cmd)
        account = result.scalar()
        account.show_secret()
        await session.commit()

async def syncRogueData(rogue: RogueBasicModel, secret: str) -> None:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        account.rlv2 = rogue.rlv2
        account.currentRogue = rogue.rlv2["current"]["game"]["theme"]
        await session.commit()
        
async def deleteRogueData(secret: str) -> None:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = await session.execute(user_cmd)
        account = result.scalar()
        account.user["rlv2"]["current"] = {}
        account.currentRogue = ""
        await session.commit()