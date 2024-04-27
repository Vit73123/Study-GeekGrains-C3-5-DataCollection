from pprint import pprint

import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

url = "https://api.giphy.com/v1/gifs/search"

params = {
    "api_key": os.getenv("API_KEY"),
    "q": "programming",
    "limit": 5,
    "offset": 0,
    "rating": "pg-13",
    "lang": "ru",
    "bundle": "messaging_non_clips",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    'Accept': "*/*",
}

response = requests.get(url=url, params=params, headers=headers)

text_data = response.text
json_data = response.json()

# response.headers
# response.status_code
# response.text
# response.content

if response.status_code == 200:
    print("Do something")
else:
    pass

if response.ok:
    print("Do something")
else:
    pass

for gif in json_data.get('data'):
    print(gif.get('images').get('original').get('url'))

with open('gifs.json', 'w') as f:
    json.dump(json_data, f)

pprint(json_data)