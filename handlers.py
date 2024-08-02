from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from slowapi import Limiter
from slowapi.util import get_remote_address

from uuid import uuid1
from database import jwt_utils as jwt


limiter = Limiter(key_func=get_remote_address)
templates = Jinja2Templates("templates")

router = APIRouter()


@router.get("/")
async def main_page(request: Request):
    response = templates.TemplateResponse(request, "index.html")
    print(request.client.host, sep="\n")
    return response


@router.get("/connect")
@limiter.limit("60/minute")
async def connect(request: Request, name: str = "DEFAULT"):
    uuid = uuid1()
    response = RedirectResponse("/")
    response.set_cookie("Authorization", jwt.gen_jwt(name=name, id=uuid))
    return response


@router.get("/chat")
@limiter.limit("60/minute")
async def chat(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context=jwt.decode_jwt(request.cookies.get("Authorization"))
    )