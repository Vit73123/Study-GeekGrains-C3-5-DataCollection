import requests
from lxml import html
from pymongo import MongoClient
import csv
from pprint import pprint
from random import randint

response = None

all_movies = []


def connect_to_imdb():
    global response

    url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
        "Accept": "*/*",
    }

    response = requests.get(
        url=url,
        headers=headers
    )


def save_to_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client['imdb_movies']
    collection = db['top_movies']
    collection.insert_many(all_movies)

    client.close()


def save_to_csv():
    with open('../../hw/movies.csv', 'w', newline='', encoding='utf8') as f:
        writer = csv.DictWriter(f,
                                fieldnames=['_id', 'name', 'release_year', 'position', 'titlemeter', 'position_change'])
        writer.writeheader()
        writer.writerows(all_movies)


def get_all():
    global response
    global all_movies

    tree = html.fromstring(html=response.content)
    movies = tree.xpath(
        '//ul[contains(@class,"ipc-metadata-list")]/li[contains(@class,"ipc-metadata-list-summary-ite")]')

    for movie in movies:
        titlemeter_t = movie.xpath(
            './div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"meter-const-ranking")]/span/svg/@class')[
            0].split()
        if 'rank-up' in titlemeter_t:
            titlemeter = 'up'
        elif 'rank-down' in titlemeter_t:
            titlemeter = 'down'
        else:
            titlemeter = 'no change'

        try:
            position_change = int(movie.xpath(
                './div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"meter-const-ranking")]/span/text()')[
                                      0])
        except:
            position_change = 'no change'

        m = {
            'name': movie.xpath(
                './/div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"ipc-title--on-textPrimary")]/a/h3/text()')[
                0],
            'release_year': int(movie.xpath(
                './/div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"cli-title-metadata")]/span[1]/text()')[
                                    0]),
            'position': int(movie.xpath(
                './div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"meter-const-ranking")]')[
                                0].text),
            'titlemeter': titlemeter,
            'position_change': position_change,
        }

        all_movies.append(m)


if __name__ == '__main__':
    connect_to_imdb()
    get_all()
    save_to_mongodb()
    save_to_csv()

    print(len(all_movies))
    print()

    index = randint(1, 100)
    print('index: ' + str(index))
    pprint(all_movies[index])
