from bson import ObjectId
from pymongo import MongoClient
from app.settings import DATABASE
from mongo.models import Result


_client = MongoClient(host=DATABASE['HOST'], port=DATABASE['PORT'])
_database = _client[DATABASE['NAME']]

_counters_collection = _database['counters']
_results_collections = _database['results']


def add_result(result: Result) -> str:
    resp = _results_collections.insert_one(result.dict())
    return str(resp.inserted_id)


def has_counter(counter_id: ObjectId) -> bool:
    if ObjectId.is_valid(counter_id):
        counter = _counters_collection.find_one({'_id': ObjectId(counter_id)})
        return bool(counter)
    return False
