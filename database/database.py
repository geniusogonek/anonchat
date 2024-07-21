import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

load_dotenv()

DB_CONNECTION = os.getenv("DB_CONNECTION")

Base = declarative_base()

engine: AsyncEngine = create_async_engine(DB_CONNECTION)