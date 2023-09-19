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

    # Round number information
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

    # Player Name
    def insert_data(self, database_name, collection_name, data):
        database, collection = self.retrieve_collection(database_name, collection_name)
        collection.insert_one(data)

    def update_score(self, database_name, collection_name, name, score):
        database, collection = self.retrieve_collection(database_name, collection_name)
        response = collection.find_one({"name": name}, {})
        print(response)
        if response != None:
            new_score = response['current_score'] + score
            search_data = {"name": name}
            updated_data = {"$set": {"current_score": new_score}}
            collection.update_one(search_data, updated_data)
        else:
            data = {
                "name": name,
                "current_score": score
            }
            collection.insert_one(data)

    def get_score_info(self, database_name, collection_name):
        database, collection = self.retrieve_collection(database_name, collection_name)
        response = collection.find()
        players = []
        for player in response:
            players.append(player)
        players.sort(key=lambda x: x["current_score"], reverse=True)
        return players