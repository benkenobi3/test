from .async_database import AsyncDatabase
from .sync_database import SyncDatabase


async_database = AsyncDatabase()
sync_database = SyncDatabase()


async def get_async_db():
    return async_database


def get_sync_db():
    return sync_database
