

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException
from pymongo import MongoClient
from pymongo.database import Database

from Project.settings import settings

# settings = Settings()


def start_db_client(app: FastAPI):
    """Create an instance of mongo client and database"""
    app.mongodb_client = MongoClient(settings.DB_URL)
    app.mongodb = app.mongodb_client.get_database(settings.DB_NAME)


def shutdown_db_client(app: FastAPI):
    """Shutdown mongo client"""
    app.mongodb_client.close()


async def get_database(request: Request) -> Database:
    """Return an instance of the MongoDB Client"""
    try:
        yield request.app.mongodb
    except AttributeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="MongoDB not initialized",
        )
