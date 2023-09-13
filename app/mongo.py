from pymongo import MongoClient
import json
from bson.json_util import dumps, loads


class Mongo:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.client = MongoClient('database', 27017, username="root", password="rootpassword")

    def retrieve_collection(self, database, collection):
        mydb = self.client[database]
        mycol = mydb[collection]
        return mycol

    def insert_player_name(self, database, collection, player_name):
        collection = self.retrieve_collection(database, collection)
        mydict = {"name": player_name}
        collection.insert_one(mydict)

    def list_players(self, database, collection):
        collection = self.retrieve_collection(database, collection)
        response = collection.find({}, {"name": 1, "_id": 0})

        player_names = []
        for doc in response:
            player_names.append(doc["name"])

        return player_names
