# # Курс: Сбор и разметка данных (семинары)
# # Урок 4. Парсинг HTML. XPath

# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.
#
# Ваш код должен включать следующее:
#
# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

import requests
from lxml import html
from pymongo import MongoClient
import csv
from pprint import pprint
from random import randint

# Ответ на запрос к сайту
response = None

# Список фильмов, полученных со страницы сайта
all_movies = []


# Запрос к сайту https://www.imdb.com
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


# Сохранение списка фимльов в базу данных MongoDB
def save_to_mongodb():
    client = MongoClient('mongodb://localhost:27017')
    db = client['imdb_movies']
    collection = db['top_movies']
    collection.insert_many(all_movies)

    client.close()


# Сохранение списка фимльов в файл csv
def save_to_csv():
    with open('../../hw/movies.csv', 'w', newline='', encoding='utf8') as f:
        # Получить объект DictWriter, описать поля
        writer = csv.DictWriter(f,
                                fieldnames=['_id', 'name', 'release_year', 'position', 'titlemeter', 'position_change'])
        writer.writeheader()
        writer.writerows(all_movies)


# Загрузить фильмы со страницы сайта в общий список фильмов all_movies
def get_all():
    global response
    global all_movies

    # Получить объект дерева HTML из запроса
    tree = html.fromstring(html=response.content)
    # Получить узел таблицы (списка) с фильмами на странице
    movies = tree.xpath(
        '//ul[contains(@class,"ipc-metadata-list")]/li[contains(@class,"ipc-metadata-list-summary-ite")]')

    # Для каждой записи в таблице (списка) с фильмами
    # получить необходимые элементы:
    # - 'name' - название фильма
    # - 'release_year' - год фильма
    # - 'position' - текущее место в рейтинге
    # - 'titlemeter' - изменение в рейтинге (рост / падение / без изменений)
    # - 'position_change' - значение изменения рейтинга
    # сохранить все элементы в запись словаря
    # и добавить каждую запись в общий список записей с фильмами all_movies

    for movie in movies:
        # Обработать в элементе span графический элемент swg об измении рейтинга
        # Получить значение в зависимости от класса элемента:
        # если есть класс 'rank-up', то присвоить значение 'up'
        # если есть класс 'rank-down', то присвоить значение 'down'
        # иначе присвоить значение 'no change'
        titlemeter_t = movie.xpath(
            './div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"meter-const-ranking")]/span/svg/@class')[
            0].split()
        if 'rank-up' in titlemeter_t:
            titlemeter = 'up'
        elif 'rank-down' in titlemeter_t:
            titlemeter = 'down'
        else:
            titlemeter = 'no change'

        # Обработать элемент span с изменением рейтинга:
        # - если в элементе есть текст, то преобразовать в число и присвоить это значение в записи о фильме
        # - если в элементе отсутствует текст, обработать исключение о ненайденном элементе списка
        #   и присвоить значение 'no change'
        try:
            position_change = int(movie.xpath(
                './div[@class="ipc-metadata-list-summary-item__c"]/div[@class="ipc-metadata-list-summary-item__tc"]/div[contains(@class,"sc-b189961a-0")]/div[contains(@class,"meter-const-ranking")]/span/text()')[
                                      0])
        except:
            position_change = 'no change'

        # Создать запись словаря с данными о фильме
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

        # Добавить запись словаря в общий список записей всех фильмов со страницы
        all_movies.append(m)


if __name__ == '__main__':
    connect_to_imdb()
    get_all()
    save_to_mongodb()
    save_to_csv()

    # Проверка:

    # Количество фильмов, полученных со страницы
    print(len(all_movies))
    print()

    # Вывод сведений о случайном фильме со страницы
    index = randint(1, 100)
    print('index: ' + str(index))
    pprint(all_movies[index])