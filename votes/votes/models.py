from votes.db import Base
from sqlalchemy import String,ForeignKey
from sqlalchemy.orm import Mapped,mapped_column

class Vote(Base):
    __tablename__ = "vote"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id:Mapped[int] = mapped_column(nullable=False)
    thumbnail_id:Mapped[String] = mapped_column(String(20),nullable=False)

class Voters(Base):
    __tablename__ = "voters"
    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vote_id: Mapped[int]  = mapped_column(ForeignKey("vote.id"))