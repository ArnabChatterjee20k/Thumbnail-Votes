from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine("sqlite:///test.db")
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def create_db():
    Base.metadata.create_all(bind=engine)