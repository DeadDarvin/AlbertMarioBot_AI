from datetime import datetime

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import SmallInteger
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    telegram_id = Column(BigInteger, primary_key=True)
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    registration_time = Column(DateTime, nullable=False, default=datetime.utcnow())
    companion_id = Column(SmallInteger, ForeignKey("persons.id"), nullable=True)
    companion = relationship("Person", uselist=False, lazy="joined")


class Person(Base):
    """Model of person for conversation with user"""

    __tablename__ = "persons"

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    first_message_text = Column(Text, nullable=False, unique=False)


class UserMessage(Base):
    """
    Contains:
        request_text - text from user. It will be sent to gpt.
        response_text - text from gpt. It will be sent to user.
    """

    __tablename__ = "user_messages"

    message_id = Column(BigInteger, primary_key=True)
    request_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=True)
    user_id = Column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    # user = relation
