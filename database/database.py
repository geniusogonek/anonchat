from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base

from config import DB_CONNECTION

Base = declarative_base()

engine: AsyncEngine = create_async_engine(DB_CONNECTION)