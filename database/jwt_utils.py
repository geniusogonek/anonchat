import jwt
from database.work import get_discord_id

from config import JWT_SECRET


async def gen_jwt(id):
    discord_id = await get_discord_id(id)
    return jwt.encode({"id": id, "discord_id": discord_id}, JWT_SECRET, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])