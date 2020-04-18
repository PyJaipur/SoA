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
from sqlalchemy.ext.hybrid import hybrid_property
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


class Checker:
    """
    Using this you can do
        
        user.is_.admin
    """

    __slots__ = ["collection", "prefix"]

    def __init__(self, collection, prefix):
        self.collection = collection
        self.prefix = prefix

    def __getattr__(self, x):
        return self.prefix + x in self.collection


class AnonUser:
    id = username = email = None
    permissions = []
    is_ = Checker(set(["is_anon"]), "is_")


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String)
    permissions = Column(JSON)
    email_hash = Column(String)
    show_email_on_cert = Column(Boolean, default=False)
    taskprogress = Column(JSON)
    last_seen = Column(DateTime)

    login_score = Column(Integer, default=0)
    task_score = Column(Integer, default=0)

    @hybrid_property
    def score(self):
        return self.login_score + self.task_score

    def ensure_email_hash(self, session):
        if self.email_hash is None:
            self.email_hash = hashlib.sha256(self.email.encode()).hexdigest()
            session.commit()

    def has_completed_task(self, task):
        if self.taskprogress is None:
            return False
        return task.slug in self.taskprogress["done"]

    def has_completed_track(self, track):
        if self.taskprogress is None:
            return False
        return all([t.slug in self.taskprogress["done"] for t in track.tasks])

    # ---------------

    @property
    def is_(self):
        return Checker(
            set(self.permissions) if self.permissions is not None else set(), "is_"
        )


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


Base.metadata.create_all(engine)
bt.common_kwargs.update(
    {"User": User, "LoginToken": LoginToken,}
)
Session = sessionmaker(engine)
