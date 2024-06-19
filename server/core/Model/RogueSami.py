from sqlalchemy import Column, Integer, String, JSON, Null
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column
from .RogueBase import RogueBase
from .User import Base

class Base(DeclarativeBase):
    pass

class RogueSami(RogueBase, Base):
    phone: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

    #def getBuffs(self):
        