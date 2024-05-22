from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.steam


def find():
    # query = {"name": {"$regex": "Puzzle"}}
    # query = {"name": {"$regex": "[Pp]uzzle"}}
    query = {"name": {"$regex": "[Pp]uzzle | [Gg]ame"}}
    games = db.games.find(query)

    num_games = 0
    for game in games:
        print(game)
        num_games += 1

    print('Число игр: %d' % num_games)


if __name__ == '__main__':
    find()
