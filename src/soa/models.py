from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from soa.settings import database_url
import bottle_tools as bt


engine = create_engine(database_url)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))


Base.metadata.create_all(engine)
bt.common_kwargs.update(Base.metadata.tables)
