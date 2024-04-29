# Урок 1. Домашнее задание
# 1. Сценарий Foursquare
# 2. Напишите сценарий на языке Python, который предложит пользователю ввести интересующую его категорию (например, кофейни, музеи, парки и т.д.).
# 3. Используйте API Foursquare для поиска заведений в указанной категории.
# 4. Получите название заведения, его адрес и рейтинг для каждого из них.
# 5. Скрипт должен вывести название и адрес и рейтинг каждого заведения в консоль.

import requests
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

url_places = "https://api.foursquare.com/v3/places"
url_places_search = url_places + "/search"

params = input("Что ищем? ")
fields = "fsq_id,name,categories,location,rating"

params = {
    "search": params,
    "fields": fields,
}

headers = {
    "Authorization": os.getenv("API_KEY"),
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    'Accept': "*/*",
}

response = requests.get(url=url_places_search, params=params, headers=headers)

if response.ok:
    json_data = response.json()
    print("Ваше местоположение: ", json_data.get('context').get('geo_bounds').get('circle'))
    print()
    for result in json_data.get('results'):
        print('Наименование: ' + result.get('name'))
        print('Категория: ' + ",".join([category.get('name') for category in result.get('categories')]))
        print('Адрес: ' + result.get('location').get('formatted_address'))
        print('Рейтинг: ' + str(result.get('rating')))
        print()
else:
    pass