"""
    Module: main.py
    Author: Rahul George

    Description:

    License:

    Created on: 11-06-2024

"""

from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ValidationStudioCloud.routers import router

from ValidationStudioCloud.settings import settings

from ValidationStudioCloud.dependencies import shutdown_db_client, start_db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handles startup and shutdown tasks for the application."""
    start_db_client(app)
    print("Application started")
    yield
    print("Application shut down")
    shutdown_db_client(app)


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

origins = ["http://localhost", "http://localhost:8000", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, reload=settings.RELOAD, port=settings.PORT)
