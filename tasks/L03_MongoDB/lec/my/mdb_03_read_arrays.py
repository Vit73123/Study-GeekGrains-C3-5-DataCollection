from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.steam


def find():
    # query = {"categories": "Co-op"}
    # query = {"categories": {"$in": ["Co-op", "Remote Play on Tablet"]}}
    # query = {"categories": {"$in": ["Co-op", "Remote Play on Tablet", "Steam Achievements"]}}
    # query = {"categories": {"$all": ["Co-op", "Remote Play on Tablet", "Steam Achievements"]}}
    query = {"categories": {"$all": ["Steam Trading Cards", "Co-op", "Remote Play on Tablet", "Steam Achievements"]}}
    games = db.games.find(query)

    num_games = 0
    for game in games:
        print(game)
        num_games += 1

    print('Число игр: %d' % num_games)


if __name__ == '__main__':
    find()
