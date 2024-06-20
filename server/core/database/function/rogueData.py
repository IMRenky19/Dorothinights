from server.core.database.function.init import sqlalchemy_config
from server.core.database.function.userData import getAccountBySecret, syncRogueData, deleteRogueData
from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
from server.core.Model.RogueBase import RogueBasicModel
#from server.core.Model.RoguePhantom import RoguePhantom
#from server.core.Model.RogueMizuki import RogueMizuki
from server.core.Model.RogueSami import RogueSami

from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy import select
from sqlalchemy.orm import Session
from .userData import get_sqlalchemy_config
from server.core.utils.json import read_json, write_json
from random import randint as rd
from server.constants import CONFIG_PATH
from time import time
from ...utils.rogueHandler.rogue_3 import createGame


session_config = AsyncSessionConfig(expire_on_commit=False)
database_config = read_json(CONFIG_PATH)["database"]


async def generateRogueData(theme: str, hardLevel: int, secret: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    account = await getAccountBySecret(secret)
    phone = account.phone
    uid = account.uid
    rlv2_data = account.user["rlv2"]
    async with config.get_session() as session:
        now_rogue = await getRogueBySecret(secret)
        if not(now_rogue):
            await giveUpRogue(secret)
        match theme:
            case "rogue_1":
                pass
            case "rogue_2":
                pass
            case "rogue_3":
                new_rogue = RogueBasicModel(
                    uid = uid,
                    phone = phone,
                    secret = secret,
                    
                    rlv2 = rlv2_data,
                    extension = {}
                )
        session.add(new_rogue)
        createGame.createGameExtra(new_rogue, hardLevel)
        await session.commit()
    await syncRogueData(new_rogue, secret)
    return new_rogue




        
async def giveUpRogue(secret: str) -> None:
    config = await get_sqlalchemy_config()
    account = await getAccountBySecret(secret)
    async with config.get_session() as session:
        match account.currentRogue:
            case "rogue_1":
                pass
            case "rogue_2":
                pass
            case "rogue_3":
                user_cmd = select(RogueBasicModel).where(RogueBasicModel.secret == secret)
                rogue_data = await session.execute(user_cmd)
                await session.delete(rogue_data)
                
    await deleteRogueData(secret)
                
async def getRogueBySecret(secret: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(RogueBasicModel).where(RogueBasicModel.secret == secret)
        result = await session.execute(user_cmd)
    return result.scalar()

#async def syncrogueData(rogue: rogueBase