import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import re

# from fake_useragent import UserAgent

# ua = UserAgent()

url = "http://books.toscrape.com"

headers = {
    # "User-Agent": ua.random,
    "User-Agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
    "Accept": "*/*",
}

params = {
}

session = requests.session()

all_books = []

page = 1
while True:
    response = session.get(url + "/catalogue/category/books_1/page-" + str(page) + ".html", params=params, headers=headers)

    if not response.ok:
        break

    soup = BeautifulSoup(response.text, 'html.parser')
    books = soup.findAll('article', {'class': 'product_pod'})

    for book in books:
        book_info = {}

        name_info = book.find('h3').find('a')
        book_info['name'] = name_info.getText()
        book_info['url'] = url + '/catalogue/' + '/'.join(name_info.get('href').split('/')[-2:])

        book_info['price'] = float(book.find('p', {'class': 'price_color'}).getText()[2:])

        response = session.get(book_info['url'], params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_page = soup.find('article', {'class': 'product_page'})

        stock_info = book_page.find('p', {'class': 'instock availability'})
        book_info['stock'] = int(re.search(r'\d+', stock_info.getText()).group(0))

        description_info = book_page.find('div', {'id': 'product_description'})
        if description_info:
            book_info['description'] = description_info.find_next_sibling('p').text
        else:
            book_info['description'] = None

        all_books.append(book_info)

    print(f"Обработано {page} страница")
    page += 1

pprint(len(all_books))
with open('books.json', 'w') as f:
    json.dump(all_books, f, indent=2)