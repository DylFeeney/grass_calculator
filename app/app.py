from flask import Flask, render_template
from pymongo import MongoClient

from players import players

app = Flask(__name__)
app.register_blueprint(players)


def create_mongo_client():
    client = MongoClient('database', 27017, username="root", password="rootpassword")
    return client


def test_insert(mongo_client):
    mydb = mongo_client["mydatabase"]
    mycol = mydb["customers"]

    mydict = {"name": "John", "address": "Highway 37"}
    x = mycol.insert_one(mydict)

    for x in mycol.find():
        print(x)


def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://user:pass@cluster.mongodb.net/myFirstDatabase"
    print("Testing 2")
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient('database', 27017, username="root", password="rootpassword")
    #client = MongoClient("mongodb://localhost:27017/")
    print("Testing 3")
    database = client["grass_database"]
    print(database.list_databases())


@app.route("/")
def hello_world():
    mongo_client = create_mongo_client()
    test_insert(mongo_client)
    #get_database()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
