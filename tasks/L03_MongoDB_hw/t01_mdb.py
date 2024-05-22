from pymongo import MongoClient
import json

client = MongoClient('mongodb://localhost:27017')
collection = client.geekbrains.books


# Загрузка данных в базу данных
def load_data():
    with open('data\\books.json', 'r', encoding='utf-8') as file:
        file_data = json.load(file)
    collection.insert_one(file_data)


# Запросы к базе данных
def test_queries():
    # Цена книги по названию
    query = {'name': 'Soumission'}
    book = collection.find_one(query)
    print(f"Цена книги 'Soumission': {book['price']}")  # 50.1

    # Все книги с ценой не выше 12 у.е
    query = {'price': {'$lte': 12}}
    books = [item for item in collection.find(query)]
    print(f"Количество книг по цене не выше 12 у.е.: {len(books)}")  # 44

    # Все книги на букв 'A'
    query = {"name": {"$regex": "A"}}
    books = [item for item in collection.find(query)]
    print(f"Количество книг на букву 'A': {len(books)}")  # 186

    # Добавить к книге жанр
    query = {'name': 'Soumission'}

    book = collection.find_one(query)
    keys = [key for key in book]
    print(keys)  # ['_id', 'name', 'url', 'price', 'stock', 'description']

    genre = ['thriller', 'detective']
    collection.update_one({'name': 'Soumission'}, {"$set": {'genre': genre}})
    book = collection.find_one(query)
    keys = [key for key in book]
    print(keys)  # ['_id', 'name', 'url', 'price', 'stock', 'description', 'genre']


if __name__ == '__main__':
    # load_data()
    test_queries()
