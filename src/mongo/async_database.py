from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from app.settings import DATABASE
from mongo.models import Result, Counter


_client = AsyncIOMotorClient(host=DATABASE['HOST'], port=DATABASE['PORT'])
_database = _client[DATABASE['NAME']]

_counters_collection = _database.get_collection('counters')
_results_collections = _database.get_collection('results')


async def add_counter(counter: Counter) -> Counter:
    resp = await _counters_collection.insert_one(counter.dict())
    counter.id = resp.inserted_id
    return counter


async def get_results(counter_id: str, time_from: int, time_to: int, with_top: bool = False) -> list:
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
        async for result in _results_collections.find(query, projection):
            results.append(result)
        return results
    return []
