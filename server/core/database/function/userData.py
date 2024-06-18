from server.core.database.function.init import sqlalchemy_config
from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
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

async def get_engine():
    engine = SQLAlchemyAsyncConfig(
                connection_string=f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}", 
                session_config=session_config,
                encoding='utf8'
            ).get_engine()
    return engine

async def generateUsers(phone: int, password: int) -> Account:
    engine = get_engine()
    secret: str = hashlib.md5((phone + decrypt_user_key(USER_TOKEN_KEY, int(time()))).encode()).hexdigest()
    async with Session(engine) as session:
        new_user = Account(
            uid=rd(10000000,1000000000),
            phone=phone,
            password=password,
            secret=secret,
            user={},
            mails=[],
            assist_char_list={},
            friend={
                'list':[],
                'request':[]
            },
            ban=0,
            notes=[]
        )
        session.add(new_user)
        session.commit()
    return new_user
        
async def getAccountBySecret(secret: str) -> Account:
    session: Session
    async with Session(get_engine()) as session:
        user_cmd = select(Account).where(Account.secret == secret)
        result = session.execute(user_cmd)
    return result.scalars[0]

async def getAccountByPhone(phone: str) -> Account:
    #session: Session
    async with Session(get_engine()) as session:
        user_cmd = select(Account).where(Account.phone == phone)
        result = session.execute(user_cmd)
    return result.scalars[0]

async def getAccountByUid(uid: str) -> Account:
    #session: Session
    async with Session(get_engine()) as session:
        user_cmd = select(Account).where(Account.uid == uid)
        result = session.execute(user_cmd)
    return result.scalars[0]
