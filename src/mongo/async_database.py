from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from bson.objectid import ObjectId
from mongo.models import Result, Counter


class AsyncDatabase:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None
    counters_collection: AsyncIOMotorCollection = None
    results_collection: AsyncIOMotorCollection = None

    def __init__(self, connection_uri: str, database_name: str):
        self.connection_uri = connection_uri
        self.database_name = database_name

    def connect_to_database(self):
        self.client = AsyncIOMotorClient(self.connection_uri)
        self.database = self.client[self.database_name]
        self.counters_collection = self.database.get_collection('counters')
        self.results_collection = self.database.get_collection('results')

    def close_database_connection(self):
        self.database.close()

    async def add_counter(self, counter: Counter) -> Counter:
        resp = await self.counters_collection.insert_one(counter.dict())
        counter.id = resp.inserted_id
        return counter

    async def get_results(self, counter_id: str, time_from: int, time_to: int, with_top: bool = False) -> list:
        if ObjectId.is_valid(counter_id):
            query = {
                'counter_id': counter_id,
                'timestamp': {'$gte': time_from, '$lte': time_to}
            }
            projection = {
                '_id': 0,
                'counter_id': 0,
                'top_ads': 0
            }

            if with_top:
                projection.pop('top_ads')

            results = []
            async for result in self.results_collection.find(query, projection):
                results.append(result)
            return results
        return []
