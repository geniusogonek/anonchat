from sqlalchemy import Column, Integer, String
from database.database import Base


class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, autoincrement=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    text = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    discord_id = Column(Integer)
    companion = Column(String)