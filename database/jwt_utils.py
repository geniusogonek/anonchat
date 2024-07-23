import jwt

from config import JWT_SECRET


async def gen_jwt(name, id):
    return jwt.encode({"name": name, "id": id}, JWT_SECRET, algorithm="HS256")


def decode_jwt(token):
    if token is None:
        return {"is_auth": False}
    return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])