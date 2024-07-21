from database.models import Chat, Message, User
from database.database import engine, Base
from database import jwt_utils as jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request


async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def reg_user(name, discord_id):
    async with AsyncSession(engine) as session:
        async with session.begin():
            user = User(name=name, discord_id=discord_id)
            session.add(user)
            await session.commit()


def get_user_id(request: Request):
    return jwt.decode_jwt(request.cookies.get("Authorization"))["id"]


async def get_discord_id(request: Request):
    async with AsyncSession(engine) as session:
        session.get(User, get_user_id(request))
        return session.discord_id


async def get_companion(request: Request):
    async with AsyncSession(engine) as session:
        session.get(User, get_user_id(request))
        return session.companion


async def check_auth(request: Request):
    async with AsyncSession(engine) as session:
        return jwt.decode_jwt (request.cookies.get("Authorization"))["id"] in [user.id for user in User.query.all()]