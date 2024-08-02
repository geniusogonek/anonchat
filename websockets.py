from typing import List
from fastapi import WebSocket, APIRouter

router = APIRouter()

class AnonChatManager:
    def __init__(self):
        self.active_connects: List[List[WebSocket]] = []
        self.waiting: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.receive()

        self.waiting.append(websocket)
        if len(self.waiting) == 2:
            (self.send(conn, "companion is founded!") for conn in self.waiting)
            self.active_connects.append(self.waiting)
            self.waiting.clear()

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

    def send_companion(self, websocket, text):
        for conn1, conn2 in self.active_connects:
            if websocket == conn1:
                self.send(conn2, text)
            if websocket == conn2:
                self.send(conn1, text)


manager = AnonChatManager()