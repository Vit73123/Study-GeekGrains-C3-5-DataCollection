from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.steam


def find():
    # query = {"developer": "Valve"}
    query = {
        "developer": "Valve",
        "genre": "Action",
    }

    projection = {"_id": 0, "name": 1}
    # games = db.games.find(query)
    games = db.games.find(query, projection)

    for a in games:
        print(a)


if __name__ == '__main__':
    find()
