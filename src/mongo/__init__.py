from mongo.async_database import AsyncDatabase
from mongo.sync_database import SyncDatabase
from app.settings import MONGO_URI, DATABASE_NAME


async_db = AsyncDatabase(MONGO_URI, DATABASE_NAME)
sync_db = SyncDatabase(MONGO_URI, DATABASE_NAME)


async def get_async_db():
    return async_db


def get_sync_db():
    return sync_db
