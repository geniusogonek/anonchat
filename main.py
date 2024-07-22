import asyncio
import uvicorn

from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Response
from fastapi.templating import Jinja2Templates
from database import work


app = FastAPI()
templates = Jinja2Templates("templates")


class AnonChatManager:
    def __init__(self):
        self.active_connects: List[List[WebSocket]] = []
        self.waiting: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.receive()

        self.waiting.append(websocket)
        if len(self.waiting) == 2:
            (self.send(conn, "companion is founded!") for conn in self.waiting)
            self.active_connects.append(self.waiting.pop())
    
    def disconnect(self, websocket):
        for index, (conn1, conn2) in enumerate(self.active_connects):
            if websocket == conn1:
                self.send(conn2, "companion_leave_you")
            elif websocket == conn2:
                self.send(conn1, "companion_leave_you")
            else:
                continue
            del self.active_connects[index]

    def disconnect_from_waiting(self, websocket):
        if websocket in self.waiting:
            self.waiting.remove(websocket)

    async def send(websocket: WebSocket, text: str):
        await websocket.send_text(text)

    def get_companion(self, websocket):
        for conn1, conn2 in self.active_connects:
            if websocket == conn1:
                return conn2
            if websocket == conn2:
                return conn1


@app.get("/chat")
async def chat(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"is_auth": await work.check_auth(request)}
    )

# TODO
# ПЕРЕПИСАТЬ
#@app.websocket("/ws")
#async def websocket_connect(websocket: WebSocket, request: Request):
#    await manager.connect(websocket)
#    try:
#        while True:
#            data = await websocket.receive_text()
#            await manager.send(f"СОБЕСЕДНИК: {data}", await work.get_companion(request))
#            await manager.send(f"ВЫ: {data}", websocket)
#    except WebSocketDisconnect:
#        manager.disconnect(websocket)
#        await manager.send("СОБЕСЕДНИК ПОКИНУЛ ЧАТ, ОБЩЕНИЕ ЗАВЕРШЕНО", await work.get_companion(request))


async def main():
    await work.init()
    uvicorn.run(app)


if __name__ == "__main__":
    asyncio.run(main())