from bson import ObjectId
from pymongo import MongoClient
from mongo.models import Result


class SyncDatabase:
    client: MongoClient = None
    database = None
    counters_collection = None
    results_collection = None

    def __init__(self, connection_uri: str, database_name: str):
        self.connection_uri = connection_uri
        self.database_name = database_name

    def connect_to_database(self):
        self.client = MongoClient(self.connection_uri)
        self.database = self.client[self.database_name]
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
