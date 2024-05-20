from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, DeclarativeBase

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=False, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)

def create_db():
    Base.metadata.create_all(bind=engine)