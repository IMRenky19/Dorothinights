from server.core.database.function.init import sqlalchemy_config
from server.core.database.function.userData import getAccountBySecret, syncRogueData, deleteRogueData
from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
from server.core.Model.RogueBase import RogueBasicModel
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from .userData import get_sqlalchemy_config
from server.core.utils.json import read_json, write_json
from random import randint as rd
from server.constants import CONFIG_PATH
from time import time
#from ...utils.rogueHandler.rogue_3 import createGame, chooseInitialRelic, chooseInitialRecruitSet, \
#    selectChoice, activeRecruitTicket, recruitChar, finishEvent, \
#        moveAndBattleStart, battleFinish, finishNodeAndEndCheck, chooseBattleReward, moveTo, buyGoods, refreshShop
from server.core.utils.rogueHandler import rogue_3


session_config = AsyncSessionConfig(expire_on_commit=False)
database_config = read_json(CONFIG_PATH)["database"]


async def generateRogueData(theme: str, hardLevel: int, secret: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    account = await getAccountBySecret(secret)
    phone = account.phone
    uid = account.uid
    rlv2_data = account.user["rlv2"]
    #print(1)
    await giveUpRogue(secret)
    async with config.get_session() as session:
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
                    theme = "rogue_3",
                    rlv2 = rlv2_data,
                    extension = {}
                )
                session.add(new_rogue)
                await rogue_3.createGameExtra(new_rogue, hardLevel)
        await session.commit()
    return new_rogue




        
async def giveUpRogue(secret: str) -> None:
    #print(2)
    config = await get_sqlalchemy_config()
    #print(3)
    async with config.get_session() as session:
        user_cmd = delete(RogueBasicModel).where(RogueBasicModel.secret == secret)
        await session.execute(user_cmd)
        await session.commit()
                
    await deleteRogueData(secret)
                
async def getRogueBySecret(secret: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    async with config.get_session() as session:
        user_cmd = select(RogueBasicModel).where(RogueBasicModel.secret == secret)
        result = await session.execute(user_cmd)
    return result.scalar()


async def rogueChooseInitialRelic(secret: str, num: int) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.chooseInitialRelic(new_rogue, num)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueChooseInitialRecruitSet(secret: str, select: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.chooseInitialRecruitSet(new_rogue, select)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueSelectChoice(secret: str, choice: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.selectChoice(new_rogue, choice)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueActiveRecruitTicket(secret: str, choice: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.activeRecruitTicket(new_rogue, choice)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueRecruitChar(secret: str, ticketId: str, choice: str, isClose = False):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.recruitChar(new_rogue, ticketId, choice, isClose)
        session.add(new_rogue)
        
        await session.commit()
    return new_rogue


async def rogueFinishEvent(secret: str):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.rlv2FinishEvent(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueMoveAndBattleStart(secret: str, position: dict):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.moveAndBattleStart(new_rogue, position)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueMoveTo(secret: str, position: dict):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.rogueMoveTo(new_rogue, position)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueBattleFinish(secret: str, battleData: str):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    account = await getAccountBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.battleFinish(new_rogue, battleData, account.user["pushFlags"]["status"])
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueFinishBattleReward(secret: str):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.finishNodeAndEndCheck(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueChooseBattleReward(secret: str, index: int, sub: int):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.chooseBattleReward(new_rogue, index, sub)
        session.add(new_rogue)
        #print(new_rogue.rlv2["current"])
        await session.commit()
    return new_rogue

async def rogueBuyGoods(secret: str, choice: int):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.buyGoods(new_rogue, choice)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueRefreshShop(secret: str):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.refreshShop(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueLeaveShop(secret: str):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            case "rogue_4": pass
            case "rogue_3":
                await rogue_3.finishNodeAndEndCheck(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue