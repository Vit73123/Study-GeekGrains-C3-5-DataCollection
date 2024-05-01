import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["steam"]
collection = db["games"]

with open('..\\data\\steam_games.json', 'r', encoding='utf-8') as file:
    file_data = json.load(file)

collection.insert_one(file_data)