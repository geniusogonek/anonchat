import asyncio
import uvicorn

from fastapi import FastAPI
from database import work
from handlers import router

app = FastAPI()

app.include_router(router)

async def main():
    await work.init()
    server = uvicorn.Server(uvicorn.Config(app))
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())