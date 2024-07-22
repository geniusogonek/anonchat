import jwt

from config import JWT_SECRET


async def gen_jwt(id):
    return jwt.encode({"id": id}, JWT_SECRET, algorithm="HS256")


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])