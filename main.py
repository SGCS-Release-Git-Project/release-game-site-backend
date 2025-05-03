from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio

from api.api_git import rgRouter


async def mInit_AppMain() -> FastAPI:

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    load_dotenv()

    app.include_router(router=rgRouter, prefix="/git")

    return app

app = asyncio.run(mInit_AppMain())