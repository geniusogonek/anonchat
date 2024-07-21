import asyncio
import uvicorn

from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.templating import Jinja2Templates
from database import work


app = FastAPI()
templates = Jinja2Templates("templates")


class ConnectionManager():
    def __init__(self) -> None:
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        self.active_connections.remove(websocket)

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"is_auth": await work.check_auth(request)}
    )


@app.websocket("/ws")
async def websocket_connect(websocket: WebSocket, request: Request):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send(f"СОБЕСЕДНИК: {data}", await work.get_companion(request))
            await manager.send(f"ВЫ: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send("СОБЕСЕДНИК ПОКИНУЛ ЧАТ, ОБЩЕНИЕ ЗАВЕРШЕНО", await work.get_companion(request))


async def main():
    await work.init()
    uvicorn.run(app)


if __name__ == "__main__":
    asyncio.run(main())