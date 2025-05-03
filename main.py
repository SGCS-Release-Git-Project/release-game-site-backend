from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from dotenv import load_dotenv
import asyncio
import uvicorn

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

if __name__ == "__main__":
    app = asyncio.run(mInit_AppMain())
    uvicorn.run(app, host="0.0.0.0", port=8011)