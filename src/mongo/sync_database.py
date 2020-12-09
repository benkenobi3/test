from bson import ObjectId
from pymongo import MongoClient
from app.settings import DATABASE
from mongo.models import Result


class SyncDatabase:
    client: MongoClient = None
    database = None
    counters_collection = None
    results_collection = None

    def connect_to_database(self):
        self.client = MongoClient(host=DATABASE['HOST'], port=DATABASE['PORT'])
        self.database = self.client[DATABASE['NAME']]
        self.counters_collection = self.database['counters']
        self.results_collection = self.database['results']

    def close_database_connection(self):
        self.database.close()

    def add_result(self, result: Result) -> str:
        resp = self.results_collection.insert_one(result.dict())
        return str(resp.inserted_id)

    def has_counter(self, counter_id: ObjectId) -> bool:
        if ObjectId.is_valid(counter_id):
            counter = self.counters_collection.find_one({'_id': ObjectId(counter_id)})
            return bool(counter)
        return False
