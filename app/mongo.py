import pymongo.errors
from pymongo import MongoClient
import json
from bson.json_util import dumps, loads


class Mongo:
    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)

    def __init__(self):
        self.client = MongoClient('database', 27017, username="root", password="rootpassword")

    def retrieve_collection(self, database_name, collection_name):
        database = self.client[database_name]
        collection = database[collection_name]
        return database, collection

    # Player Name
    def insert_player_name(self, database_name, collection_name, player_name):
        database, collection = self.retrieve_collection(database_name, collection_name)
        mydict = {"name": player_name}
        collection.insert_one(mydict)

    def list_players(self, database_name, collection_name):
        database, collection = self.retrieve_collection(database_name, collection_name)
        response = collection.find({}, {"name": 1, "_id": 0})

        player_names = []
        for doc in response:
            player_names.append(doc["name"])

        return player_names

    def retrieve_round_number(self, database_name):
        round_numbers = "round_numbers"
        database, collection = self.retrieve_collection(database_name, round_numbers)
        try:
            database.validate_collection(round_numbers)
        except pymongo.errors.OperationFailure:  # Collection does not exist yet
            return self.insert_first_round(collection)

        response = collection.find_one({}, {"round_number": 1, "_id": 0})
        return response["round_number"]


    def insert_first_round(self, collection):
        data_to_insert = {"round_number": 1}
        collection.insert_one(data_to_insert)
        return 1

    def update_round_number(self, database_name, current_round_number):
        new_round_number = current_round_number + 1
        database, collection = self.retrieve_collection(database_name, "round_numbers")
        old_data = {"round_number": current_round_number}
        new_data = {"$set": {"round_number": new_round_number}}
        collection.update_one(old_data, new_data)
