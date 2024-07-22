from .activeRecruitTicket import activeRecruitTicket
#from .bankWithdraw import bankWithdraw
from .battleFinish import battleFinish
from .buyGoods import buyGoods
from .chooseBattleReward import chooseBattleReward
from .chooseInitialRecruitSet import chooseInitialRecruitSet
from .chooseInitialRelic import chooseInitialRelic
from .confirmPredict import confirmPredict
from .finishBattleReward import finishBattleReward
from .finishEvent import finishEvent
from .gameSettle import gameSettle
#from .getTicketAssistList import getTicketAssistList
from .leaveShop import leaveShop
from .moveAndBattleStart import moveAndBattleStart
from .moveTo import moveTo
#from .readEndingChange import readEndingChange
from .recruitChar import recruitChar
from .refreshShop import refreshShop
from .shopAction import shopAction
from .selectChoice import selectChoice
#from .shopBattleStart import shopBattleStart
from .useTotem import useTotem
from .giveUpGame import giveUpGame
from .createGame import createGame
from .closeRecruitTicket import closeRecruitTicket

from litestar import Router

router = Router(
    path = "/rlv2",
    route_handlers = [
        activeRecruitTicket,
        #bankWithdraw,
        battleFinish,
        buyGoods,
        chooseBattleReward,
        chooseInitialRecruitSet,
        chooseInitialRelic,
        closeRecruitTicket,
        confirmPredict,
        finishBattleReward,
        finishEvent,
        gameSettle,
        #getTicketAssistList,
        leaveShop,
        moveAndBattleStart,
        moveTo,
        #readEndingChange,
        recruitChar,
        refreshShop,
        selectChoice,
        #shopBattleStart,
        useTotem,
        giveUpGame,
        createGame,
        shopAction
    ]
)
