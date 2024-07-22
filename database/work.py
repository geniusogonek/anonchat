from database.models import Chat, Message
from database.database import engine, Base
from database import jwt_utils as jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_user_id(request: Request):
    return jwt.decode_jwt(request.cookies.get("Authorization"))["id"]