from typing import List
from sqlalchemy import Column, Integer, String, JSON, Null
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from .User import Base
from ..utils.time import time

ts = time()

class RogueBasicModel(Base):
    __tablename__ = "rogue"
    __table_args__ = {
        "mysql_charset": "utf8mb4"
    }
    uid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    phone: Mapped[str] = mapped_column(String(255))
    secret: Mapped[str] = mapped_column(String(255))
    
    
    rlv2: Mapped[str] = mapped_column(JSON)
    extension: Mapped[str] = mapped_column("extension",JSON)
    
    
    
    
    
    #state: Mapped[str] = mapped_column(String(16))
    #exp: Mapped[int] = mapped_column(default=Null)
    #level: Mapped[int] = mapped_column(default=Null)
    #max_level: Mapped[int] = mapped_column(default=Null)
    #hp_current: Mapped[int] = mapped_column(default=Null)
    #hp_max: Mapped[int] = mapped_column(default=Null)
    #gold: Mapped[int] = mapped_column(default=Null)
    #shield: Mapped[int] = mapped_column(default=Null)
    #capacity: Mapped[int] = mapped_column(default=Null)
    #population_cost: Mapped[int] = mapped_column(default=Null)
    #population_max: Mapped[int] = mapped_column(default=Null)
    #conPerfectBattle: Mapped[int] = mapped_column(default=Null)
    #
    #
    #cursor: Mapped[str] = mapped_column(JSON)
    #trace: Mapped[List["Node"]] = relationship(back_populates="user")
    
#class Node(Base):
#    
#    __tablename__ = "node"
#    zone: Mapped[str] = mapped_column(String(16))
#    position: Mapped[str] = mapped_column(JSON)
#    
#    user: Mapped["RogueBase"] = relationship(back_populates="trace")