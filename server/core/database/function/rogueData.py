from server.core.database.function.init import sqlalchemy_config
from server.core.database.function.userData import getAccountBySecret, syncRogueData, deleteRogueData
from server.core.utils.accounts import decrypt_user_key
from server.core.Model.User import Account
from server.core.Model.RogueBase import RogueBasicModel
from litestar.contrib.sqlalchemy.plugins import AsyncSessionConfig, SQLAlchemyAsyncConfig, SQLAlchemyInitPlugin
from sqlalchemy import select, delete, Result, Tuple
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
#from server.core.utils.rogueHandler import rogue_4
import json


session_config = AsyncSessionConfig(expire_on_commit=False)
database_config = read_json(CONFIG_PATH)["database"]

async def generateRogueData(theme: str, hardLevel: int, secret: str) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    account = await getAccountBySecret(secret)
    phone = account.phone
    uid = account.uid
    user: dict = account.user
    rlv2_data = user["rlv2"]
    await giveUpRogue(secret)
    async with config.get_session() as session:
        match theme:
            #case "rogue_1":
            #    pass
            #case "rogue_2":
            #    pass
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
            case _:
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
    config = await get_sqlalchemy_config()
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
    finalResult = result.scalar()
    if not finalResult:
        return RogueBasicModel()
    else:
        return finalResult


async def rogueChooseInitialRelic(secret: str, num: int) -> RogueBasicModel:
    config = await get_sqlalchemy_config()
    new_rogue: RogueBasicModel = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            #case "rogue_4": 
            #    await rogue_4.chooseInitialRelic(new_rogue, num)
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
            #case "rogue_4":
            #    await rogue_4.chooseInitialRecruitSet(new_rogue, select)
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
            #case "rogue_4":
            #    await rogue_4.selectChoice(new_rogue, choice)
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
            #case "rogue_4": 
            #    await rogue_4.activeRecruitTicket(new_rogue, choice)
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
            #case "rogue_4": 
            #    await rogue_4.recruitChar(new_rogue, ticketId, choice, isClose)
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
            #case "rogue_4":
            #    await rogue_4.rlv2FinishEvent(new_rogue)
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
            #case "rogue_4":
            #    await rogue_4.moveAndBattleStart(new_rogue, position)
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
            #case "rogue_4":
            #    await rogue_4.rogueMoveTo(new_rogue, position)
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
            #case "rogue_4":
            #    await rogue_4.battleFinish(new_rogue, battleData, account.user["pushFlags"]["status"])
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
            #case "rogue_4":
            #    await rogue_4.finishNodeAndEndCheck(new_rogue)
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
            #case "rogue_4":
            #    await rogue_4.chooseBattleReward(new_rogue, index, sub)
            case "rogue_3":
                await rogue_3.chooseBattleReward(new_rogue, index, sub)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueBuyGoods(secret: str, choice: int):
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        match new_rogue.theme:
            #case "rogue_4":
            #    await rogue_4.buyGoods(new_rogue, choice)
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
            #case "rogue_4":
            #    await rogue_4.refreshShop(new_rogue)
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
            #case "rogue_4":
            #    await rogue_4.finishNodeAndEndCheck(new_rogue)
            case "rogue_3":
                await rogue_3.finishNodeAndEndCheck(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueConfirmPredict(secret: str):         #ROGUE_3独有内容
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        await rogue_3.confirmPredict(new_rogue)
        session.add(new_rogue)
        await session.commit()
    return new_rogue

async def rogueUseTotem(secret: str, totemIndex: list, nodeIndex: list):         #ROGUE_3独有内容
    config = await get_sqlalchemy_config()
    new_rogue = await getRogueBySecret(secret)
    async with config.get_session() as session:
        await rogue_3.useTotem(new_rogue, totemIndex, nodeIndex)
        session.add(new_rogue)
        await session.commit()
    return new_rogue