from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker
from soa.settings import database_url
import bottle_tools as bt

engine = create_engine(database_url)
Base = declarative_base()


class AnonUser:
    id = username = email = None
    permissions = []


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    permissions = Column(JSON)


class Group(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    permissions = Column(JSON)


class UserGroupMembership(Base):
    __tablename__ = "usergroup"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    start = Column(DateTime(timezone=True))
    end = Column(DateTime(timezone=True))


Base.metadata.create_all(engine)
bt.common_kwargs.update(Base.metadata.tables)
Session = sessionmaker(engine)
