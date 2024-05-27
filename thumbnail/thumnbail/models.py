from thumnbail.db import Base
from sqlalchemy import String , ForeignKey , PrimaryKeyConstraint
from sqlalchemy.orm import Mapped,mapped_column, relationship
class Project(Base):
    __tablename__ = "project"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(30),nullable=False)
    model:Mapped[str] = mapped_column(String(30),nullable=False)
    message:Mapped[str] = mapped_column(String(120),nullable=False)
    count:Mapped[int]
    thumbnails:Mapped[list["Thumbnail"]] = relationship(backref = "thumbnails")
    workers:Mapped[list["Workers"]] = relationship(backref = "workers")
class Thumbnail(Base):
    __tablename__ = "thumbnail"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    image_id:Mapped[str] = mapped_column(String(10),nullable=True)
    project_id:Mapped[int] = mapped_column(ForeignKey("project.id"))


class Workers(Base):
    __tablename__ = "workers"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    worker_id:Mapped[str] = mapped_column(String(20),nullable=False)
    project_id:Mapped[int] = mapped_column(ForeignKey("project.id"),unique=True,nullable=False)