import asyncio
import uvicorn

from fastapi import FastAPI
from database import work
from handlers import router as base_router
from websockets import router as websockets_router

app = FastAPI()

app.include_router(base_router)
app.include_router(websockets_router)


async def main():
    await work.init()
    server = uvicorn.Server(uvicorn.Config(app))
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())