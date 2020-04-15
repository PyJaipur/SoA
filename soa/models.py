import hashlib
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker, relationship
from soa.settings import database_url
import bottle_tools as bt
from secrets import token_urlsafe

engine = create_engine(database_url)
Base = declarative_base()


def get_or_create(session, model, defaults, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance is None:
        instance = model(**defaults)
        session.add(instance)
        session.commit()
    return instance


class AnonUser:
    id = username = email = None
    permissions = []
    is_anon = True


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    permissions = Column(JSON)
    email_hash = Column(String)

    def ensure_email_hash(self, session):
        if self.email_hash is None:
            self.email_hash = hashlib.sha256(self.email.encode()).hexdigest()
            session.commit()

    # ---------------
    is_anon = False


class LoginToken(Base):
    __tablename__ = "logintoken"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    otp = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)
    is_consumed = Column(Boolean, default=False)
    has_logged_out = Column(Boolean, default=False)
    user = relationship("User")

    @staticmethod
    def loop_create(session, **kwargs):
        "Try to create a token and retry if uniqueness fails"
        while True:
            tok = LoginToken(otp=token_urlsafe(), token=token_urlsafe(), **kwargs)
            session.add(tok)
            session.commit()
            return tok


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
bt.common_kwargs.update({"User": User, "LoginToken": LoginToken})
Session = sessionmaker(engine)
