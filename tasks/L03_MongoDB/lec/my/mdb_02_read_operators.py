from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.steam


def find():
    # query = {"positive": {"$gt": 500000, "$lte": 600000}}
    # query = {"name": {"$gte": "A", "$lt": "C"}}
    query = {"required_age": {"$ne": 0}}
    games = db.games.find(query)

    num_games = 0
    for game in games:
        print(game)
        num_games += 1

    print('Число игр: %d' % num_games)


if __name__ == '__main__':
    find()
